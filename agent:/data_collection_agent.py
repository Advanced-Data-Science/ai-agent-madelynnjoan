"""
Maddy Smith CS3870
AI Data Collection Agent - NORS Data Set
Note: No API key needed
"""

import os
import json
import logging
import requests
import time
import random
from datetime import datetime

## Part 4: Build Your AI Data Collection Agent (35 points)

class DataCollectionAgent:
    #### 1. Configuration Management
    def __init__(self, config_file="config.json"):
        """Initialize data collection agent"""
        # Setup logging
        self.setup_logging()
        self.logger.info("Logger initialized")

        # Load config file, no hardcoding
        self.config = self.load_config(config_file)
        self.data_store = []
        self.collection_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0
        }

        self.logger.info("Agent initialized")
    def setup_logging(self):
        """Setup logging for the agent"""
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler("collection.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("DataCollectionAgent")

    def load_config(self, config_file):
        """Load collection parameters from JSON config"""
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
                self.logger.info(f"Config loaded from {config_file}")
                return config
        else:
            self.logger.error(f"Config file '{config_file}' not found.")
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

    ### 2. Intelligent Collection Strategy
    def collect_data(self):
        """Collect one batch of data, filter columns, store, and save to JSON"""
        data = self.make_api_request()
        if data:
            columns = self.config.get("columns", [])
            # Filter only the selected columns
            clean_data = [
                {k: v for k, v in record.items() if k in columns}
                for record in data
            ]
            self.data_store = clean_data
            print(f"Collected {len(self.data_store)} records for {self.config.get('state')} in {self.config.get('year')}")
            self.save_to_file(f"cdc_{self.config.get('state')}_{self.config.get('year')}.json")
        else:
            print("No data collected.")
            self.logger.warning("No data collected from API.")
            
    ### 3. Data Quality Assesment
    def assess_data_quality(self):
        """Evaluate the quality of collected data"""
        if not self.data_store:
            self.logger.warning("No data available to assess quality.")
            return 0

        quality_metrics = {
            'completeness': self.check_completeness(),
            'accuracy': self.check_accuracy(),
            'consistency': self.check_consistency(),
            'timeliness': self.check_timeliness()
        }

        overall_score = sum(quality_metrics.values()) / len(quality_metrics)
        self.logger.info(f"Data quality assessed: {quality_metrics}, overall score = {overall_score:.2f}")
        return overall_score

    def check_completeness(self):
        """Check if required fields are present in all records"""
        required_columns = self.config.get("columns", [])
        if not self.data_store:
            return 0
        total = len(self.data_store)
        complete = sum(1 for record in self.data_store if all(col in record and record[col] for col in required_columns))
        return complete / total

    def check_accuracy(self):
        """Placeholder"""
        # For now, just return 1.0 (assume accurate)
        return 1.0

    def check_consistency(self):
        """Check if fields have consistent formats"""
        try:
            years = {record.get("year") for record in self.data_store}
            return 1.0 if len(years) == 1 else 0.5
        except Exception:
            return 0.0

    def check_timeliness(self):
        """Check if data year matches config year"""
        year = str(self.config.get("year"))
        timely = sum(1 for record in self.data_store if record.get("year") == year)
        return timely / len(self.data_store) if self.data_store else 0
    
    ### 4. Adaptive Strategy
    def adjust_strategy(self):
        """Modify collection approach based on performance"""
        success_rate = self.get_success_rate()
    
        if success_rate < 0.5:
            # Increase delays
            self.delay_multiplier *= 2
            # Have no fallback API
        elif success_rate > 0.9:
            # Can be more aggressive
            self.delay_multiplier *= 0.8
    
        # Log strategy changes
        self.logger.info(f"Adaptive strategy applied. Delay multiplier is now {self.delay_multiplier:.2f}")

    def get_success_rate(self):
        """Return ratio of successful requests to total"""
        total = self.collection_stats.get('total_requests', 0)
        if total == 0:
            return 1.0  # Assume perfect if nothing attempted yet
        return self.collection_stats.get('successful_requests', 0) / total
            
    ### 5. Respectful Collection
    def respectful_delay(self):
        """Implement respectful rate limiting"""
        base_delay = self.config.get('base_delay', 1.0)
        delay = base_delay * self.delay_multiplier
    
        # Add random jitter to avoid thundering herd
        jitter = random.uniform(0.5, 1.5)
        time.sleep(delay * jitter)
        self.logger.info(f"Respectful delay applied: {delay * jitter:.2f} seconds")

    def check_rate_limits(self):
        """Monitor and respect API rate limits"""
        # Placeholder, API is free and has no limits
        self.logger.info("Checked API rate limits (placeholder).")
       
    ### API request
    def make_api_request(self):
        """Make API request to CDC resource endpoint"""
        self.collection_stats['total_requests'] += 1
        base_url = self.config.get("api_endpoint")
        year = self.config.get("year")
        state = self.config.get("state")
        url = f"{base_url}?year={year}&state={state}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.collection_stats['successful_requests'] += 1
            self.logger.info(f"Data successfully fetched from {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.collection_stats['failed_requests'] += 1
            self.logger.error(f"Request failed: {e}")
            return None

    ### Save to JSON
    def save_to_file(self, filename="output.json"):
        """Save collected data to JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump(self.data_store, f, indent=4)
            self.logger.info(f"Data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")

## Part 5: Documentation and Quality Assurance (20 points)
    ### 1. Automated Metadata Generation
    def generate_metadata(self):
        """Create comprehensive metadata for collected dataset"""
        metadata = {
            'collection_info': {
            'collection_date': datetime.now().isoformat(),
            'agent_version': '1.0',
            'collector': 'Maddy Smith',
            'total_records': len(self.data_store)
        },
        'data_sources': self.get_sources_used(),
        'quality_metrics': self.calculate_final_quality_metrics(),
        'processing_history': self.get_processing_log(),
        'variables': self.generate_data_dictionary()
    }
    
        filename = f"metadata_{self.config.get('state')}_{self.config.get('year')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(metadata, f, indent=2)
            self.logger.info(f"Metadata saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")
        
    def get_sources_used(self):
        """Return list of sources used (placeholder)"""
        return [self.config.get("api_endpoint")]

    def calculate_final_quality_metrics(self):
        """Return data quality metrics (reuse your assessment)"""
        return self.assess_data_quality()

    def get_processing_log(self):
        """Return processing history log (placeholder)"""
        return ["Data collected", "Columns filtered", "Saved to JSON"]

    def generate_data_dictionary(self):
        """Return list of variables/columns"""
        return self.config.get("columns", [])


    ### 2. Quality Report Generation
    def generate_quality_report(self):
        """Create detailed quality assessment report and save as HTML"""
        report = {
            'summary': {
                'total_records': len(self.data_store),
                'collection_success_rate': self.get_success_rate(),
                'overall_quality_score': self.get_overall_quality_score()
            },
            'completeness_analysis': self.analyze_completeness(),
            'data_distribution': self.analyze_distribution(),
            'anomaly_detection': self.detect_anomalies()
        }

        # Save as HTML
        filename_html = f"quality_report.html"
        try:
            with open(filename_html, 'w') as f:
                f.write("<html><head><title>Quality Report</title></head><body>\n")
                f.write(f"<h1>Quality Report - {self.config.get('state')} ({self.config.get('year')})</h1>\n")
            
                # Summary
                f.write("<h2>Summary</h2><ul>\n")
                for k, v in report['summary'].items():
                    if isinstance(v, float):
                        f.write(f"<li>{k}: {v:.2f}</li>\n")
                    else:
                        f.write(f"<li>{k}: {v}</li>\n")
                f.write("</ul>\n")

                # Other sections
                for section in ['completeness_analysis', 'data_distribution', 'anomaly_detection']:
                    f.write(f"<h2>{section.replace('_',' ').title()}</h2><pre>{report[section]}</pre>\n")
            
                f.write("</body></html>")
            self.logger.info(f"Quality report saved to {filename_html}")
        except Exception as e:
            self.logger.error(f"Failed to save quality report HTML: {e}")

        
    def get_overall_quality_score(self):
        return self.assess_data_quality()

    def analyze_completeness(self):
        return {'completeness': self.check_completeness()}

    def analyze_distribution(self):
        """Placeholder: summarize values per column"""
        distribution = {}
        if not self.data_store:
            return distribution
        for col in self.config.get("columns", []):
            values = [record.get(col) for record in self.data_store if col in record]
            distribution[col] = {'unique_values': len(set(values)), 'sample_values': values[:5]}
        return distribution

    def detect_anomalies(self):
        """Placeholder: check for missing or weird data"""
        return {'missing_records': sum(1 for r in self.data_store if not r)}

    def create_readable_report(self, report):
        """Save a simple human-readable version"""
        filename_txt = f"quality_report_{self.config.get('state')}_{self.config.get('year')}.txt"
        try:
            with open(filename_txt, 'w') as f:
                for section, content in report.items():
                    f.write(f"{section.upper()}:\n{content}\n\n")
            self.logger.info(f"Human-readable report saved to {filename_txt}")
        except Exception as e:
            self.logger.error(f"Failed to save human-readable report: {e}")


if __name__ == "__main__":
    agent = DataCollectionAgent()
    agent.collect_data()
    agent.generate_metadata()
    agent.generate_quality_report()

