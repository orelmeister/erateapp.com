"""
LLM Analyzer for USAC Data
Uses DeepSeek Reasoner to answer natural language questions about E-Rate data
"""
import json
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMAnalyzer:
    """Analyze E-Rate data using DeepSeek Reasoner"""
    
    def __init__(self):
        """Initialize DeepSeek analyzer"""
        self.client = None
        self.last_analysis = None  # Store last analysis for export
        self._setup_client()
    
    def _setup_client(self):
        """Setup DeepSeek client"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            try:
                import openai
                self.client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com"
                )
            except ImportError:
                print("⚠ OpenAI library needed for DeepSeek. Run: pip install openai")
        else:
            print("⚠ DEEPSEEK_API_KEY not found in .env file")
    
    def analyze_data(self, data: List[Dict], question: str, max_records: int = 100) -> str:
        """
        Analyze data using LLM
        
        Args:
            data: List of E-Rate records
            question: Natural language question about the data
            max_records: Maximum records to send to LLM
            
        Returns:
            LLM response
        """
        if not self.client:
            return self._fallback_analysis(data, question)
        
        # Prepare data context (limit size for token efficiency)
        data_sample = data[:max_records] if len(data) > max_records else data
        
        # Create data summary for context
        data_summary = self._create_data_summary(data)
        
        prompt = f"""You are analyzing E-Rate funding data from USAC (Universal Service Administrative Company).

DATA SUMMARY:
{data_summary}

SAMPLE RECORDS (showing {len(data_sample)} of {len(data)} total):
{json.dumps(data_sample, indent=2)}

USER QUESTION: {question}

Please analyze the data and provide a clear, detailed answer to the user's question. Include:
1. Direct answer to the question
2. Relevant statistics and insights
3. Key findings or patterns
4. Any notable observations

Be specific and use the actual data in your response."""

        try:
            response = self.client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            analysis = response.choices[0].message.content
            
            # Store for export
            self.last_analysis = {
                "question": question,
                "analysis": analysis,
                "data_count": len(data),
                "data": data
            }
            
            return analysis
        
        except Exception as e:
            print(f"⚠ DeepSeek error: {e}")
            return self._fallback_analysis(data, question)
    
    def _create_data_summary(self, data: List[Dict]) -> str:
        """Create a summary of the dataset"""
        if not data:
            return "No data available"
        
        total = len(data)
        
        # Count by status
        status_counts = {}
        for record in data:
            status = record.get("form_471_frn_status_name", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count by state
        state_counts = {}
        for record in data:
            state = record.get("state", "Unknown")
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # Calculate funding totals
        total_requested = sum(
            float(record.get("funding_commitment_request", 0) or 0)
            for record in data
        )
        
        summary = f"""Total Records: {total}
Funding Status Distribution:
{json.dumps(status_counts, indent=2)}

Top 10 States:
{json.dumps(dict(sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:10]), indent=2)}

Total Funding Requested: ${total_requested:,.2f}
Average Funding per Application: ${total_requested/total:,.2f} (if total > 0)
"""
        return summary
    
    def _fallback_analysis(self, data: List[Dict], question: str) -> str:
        """Fallback analysis without LLM"""
        summary = self._create_data_summary(data)
        
        return f"""⚠ DeepSeek not configured. Basic analysis:

{summary}

To use AI-powered analysis:
1. Get API key from: https://platform.deepseek.com/
2. Add to .env: DEEPSEEK_API_KEY=your_key_here
3. Restart the bot

Your question: "{question}"

For specific queries, try the structured query mode (option 1) in the main menu."""
