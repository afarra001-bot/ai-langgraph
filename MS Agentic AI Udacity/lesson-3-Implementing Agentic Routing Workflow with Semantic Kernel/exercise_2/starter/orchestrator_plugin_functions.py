import os
import asyncio
import re
import numpy as np
from dotenv import load_dotenv
from typing import Annotated, List

from semantic_kernel import <TODO> # Import Kernel class
from semantic_kernel.agents import <TODO> # Import Chat Completion Agent class
from semantic_kernel.connectors.ai.open_ai import <TODO> # Import Azure Chat Completion class
from semantic_kernel.functions import <TODO> # Import kernel function decorator

# -----------------
# Load Environmental Variables
# -----------------
load_dotenv()

api_key = os.getenv("AZURE_OPENAI_KEY")
url = os.getenv("URL")
api_version = "2024-12-01-preview"

# -----------------
# Initialize the kernel
# -----------------
kernel = <TODO> # Create a new kernel instance

# -----------------
# Define a chat service
# -----------------
chat_service = <TODO>( # Create Azure chat completion service
    deployment_name="none", 
    api_key=api_key,
    base_url=url,
    api_version=api_version  
)

# -----------------
# Register the chat service in the kernel
# -----------------
kernel.<TODO> # Register the chat service

# -----------------
# Create Plugin Classes with Kernel Functions
# -----------------
class OutlierRemovalPlugin:
    """Plugin for handling outlier removal operations"""
    
    @<TODO>( # Decorator to define a kernel function
        name="remove_outliers",
        description="Provides methods for detecting and removing outliers from datasets"
    )
    def remove_outliers(
        self, 
        request: Annotated[str, "The user's request about outlier removal"]
    ) -> str:
        """Remove outliers from dataset using statistical methods"""
        print(" FUNCTION CALLED: remove_outliers (General guidance)")
        <TODO> ("Use IQR method: Remove data points below Q1-1.5*IQR or above Q3+1.5*IQR, " # Return general guidance
                "or use Z-score method: Remove data points with |z-score| > 3.")

class MissingDataPlugin:
    """Plugin for handling missing data operations"""
    
    @kernel_function(
        name="handle_missing_data",
        description="Provides methods for handling missing data in datasets through various imputation techniques"
    )
    def handle_missing_data(
        self, 
        request: Annotated[str, "The user's request about missing data handling"]
    ) -> str:
        """Handle missing data using appropriate imputation methods"""
        print(" FUNCTION CALLED: handle_missing_data")
        <TODO> ("Use mean/median imputation for numerical data, mode imputation for categorical data, " # Return general guidance
                "or forward/backward fill for time series data.")

class OutlierDetectionExecutorPlugin:
    """Plugin for executing outlier detection on actual numerical data"""
    
    def _extract_numbers_from_text(self, text: str) -> List[float]:
        """Extract numerical lists from text using regex and ast parsing"""
        # Pattern to match lists like [1,2,3] or [1, 2, 3] or (1,2,3)
        list_patterns = [
            r'\[([^\]]+)\]',  # Square brackets
            r'\(([^\)]+)\)',  # Parentheses
        ]
        
        numbers = []
        
        for pattern in list_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    # Split by comma and try to convert to numbers
                    str_numbers = [s.strip() for s in match.split(',')]
                    for num_str in str_numbers:
                        try:
                            # Try to convert to float
                            numbers.append(float(num_str))
                        except ValueError:
                            continue
                except Exception:
                    continue
        
        # Also look for space-separated numbers
        if not numbers:
            # Look for sequences of numbers separated by spaces or commas
            number_pattern = r'-?\d+(?:\.\d+)?'
            found_numbers = re.findall(number_pattern, text)
            if len(found_numbers) > 2:  # Only consider if we have multiple numbers
                try:
                    numbers = [float(n) for n in found_numbers[:20]]  # Limit to first 20 numbers
                except ValueError:
                    pass
        
        return <TODO> # Return the list of extracted numbers
    
    def _detect_outliers_iqr(self, data: List[float]) -> dict:
        """Detect outliers using IQR method"""
        if len(data) < 4:
            return {
                'method': 'IQR',
                'original_data': data,
                'outliers': [],
                'cleaned_data': data,
                'message': 'Not enough data points for IQR outlier detection (minimum 4 required)'
            }
        
        # Convert to numpy array for easier calculation
        arr = np.array(data)
        
        # Calculate quartiles
        Q1 = np.percentile(arr, 25)
        Q3 = np.percentile(arr, 75)
        IQR = Q3 - Q1
        
        # Define outlier bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Identify outliers and clean data
        outliers = [x for x in data if x < lower_bound or x > upper_bound]
        cleaned_data = [x for x in data if lower_bound <= x <= upper_bound]
        
        return {
            'method': 'IQR',
            'original_data': data,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers': outliers,
            'cleaned_data': cleaned_data,
            'outliers_removed': len(outliers)
        }
    
    def _detect_outliers_zscore(self, data: List[float]) -> dict:
        """Detect outliers using Z-score method"""
        if len(data) < 3:
            return {
                'method': 'Z-Score',
                'original_data': data,
                'outliers': [],
                'cleaned_data': data,
                'message': 'Not enough data points for Z-score outlier detection (minimum 3 required)'
            }
        
        # Convert to numpy array
        arr = np.array(data)
        
        # Calculate mean and standard deviation
        mean = np.mean(arr)
        std = np.std(arr)
        
        if std == 0:
            return {
                'method': 'Z-Score',
                'original_data': data,
                'outliers': [],
                'cleaned_data': data,
                'message': 'All values are identical, no outliers detected'
            }
        
        # Calculate Z-scores
        z_scores = np.abs((arr - mean) / std)
        
        # Identify outliers (|z-score| > 3)
        outlier_mask = z_scores > 3
        outliers = arr[outlier_mask].tolist()
        cleaned_data = arr[~outlier_mask].tolist()
        
        return {
            'method': 'Z-Score',
            'original_data': data,
            'mean': mean,
            'std': std,
            'threshold': 3,
            'outliers': outliers,
            'cleaned_data': cleaned_data,
            'outliers_removed': len(outliers)
        }
    
    @<TODO>( # Decorator to define a kernel function
        name="execute_outlier_removal",
        description="Detects numerical data in text and removes outliers using statistical methods. Use when user provides actual numbers and asks to remove outliers."
    )
    def execute_outlier_removal(
        self, 
        request: Annotated[str, "The user's request containing numerical data and outlier removal instruction"]
    ) -> str:
        """Execute outlier removal on numerical data found in the request"""
        
        print(" FUNCTION CALLED: execute_outlier_removal (Processing actual data)")
        
        # Extract numbers from the text
        numbers = self._extract_numbers_from_text(request)
        
        if not numbers:
            return ("No numerical data found in your request. Please provide data in format like [1,2,3,4,5] "
                   "or specify numbers clearly for outlier removal.")
        
        if len(numbers) < 3:
            return f"Found only {len(numbers)} number(s): {numbers}. Need at least 3 data points for meaningful outlier detection."
        
        print(f" Processing {len(numbers)} data points: {numbers}")
        
        # Apply both IQR and Z-score methods
        iqr_results = self._detect_outliers_iqr(numbers)
        zscore_results = self._detect_outliers_zscore(numbers)
        
        # Format the results
        result = f"**Outlier Detection Results**\n\n"
        result += f"Original Data: {numbers}\n"
        result += f"Data Points: {len(numbers)}\n\n"
        
        # IQR Method Results
        result += f"**IQR Method:**\n"
        if 'message' in iqr_results:
            result += f"- {iqr_results['message']}\n"
        else:
            result += f"- Q1: {iqr_results['Q1']:.2f}\n"
            result += f"- Q3: {iqr_results['Q3']:.2f}\n"
            result += f"- IQR: {iqr_results['IQR']:.2f}\n"
            result += f"- Bounds: [{iqr_results['lower_bound']:.2f}, {iqr_results['upper_bound']:.2f}]\n"
            result += f"- Outliers Found: {iqr_results['outliers']} ({iqr_results['outliers_removed']} removed)\n"
            result += f"- Cleaned Data: {iqr_results['cleaned_data']}\n"
        
        result += f"\n**Z-Score Method (threshold=3):**\n"
        if 'message' in zscore_results:
            result += f"- {zscore_results['message']}\n"
        else:
            result += f"- Mean: {zscore_results['mean']:.2f}\n"
            result += f"- Std Dev: {zscore_results['std']:.2f}\n"
            result += f"- Outliers Found: {zscore_results['outliers']} ({zscore_results['outliers_removed']} removed)\n"
            result += f"- Cleaned Data: {zscore_results['cleaned_data']}\n"
        
        # Summary recommendation
        result += f"\n**Recommendation:**\n"
        if iqr_results.get('outliers_removed', 0) > 0 or zscore_results.get('outliers_removed', 0) > 0:
            result += f"Both methods detected outliers. Choose the method that best fits your data distribution:\n"
            result += f"- Use IQR method if your data might be skewed\n"
            result += f"- Use Z-score method if your data is approximately normal\n"
        else:
            result += f"No outliers detected by either method. Your data appears to be clean!"
        
        return result

class DataVisualizationPlugin:
    """Plugin for data visualization operations"""
    
    @<TODO>( # Decorator to define a kernel function
        name="visualize_data",
        description="Provides guidance on data visualization techniques and tools"
    )
    def visualize_data(
        self, 
        request: Annotated[str, "The user's request about data visualization"]
    ) -> str:
        """Provide data visualization guidance"""
        print(" FUNCTION CALLED: visualize_data")
        return "You use matplotlib for plotting your data."

# -----------------
# Create Plugin Instances
# -----------------
outlier_plugin = <TODO> # Instance of Outlier Removal Plugin
missing_data_plugin = <TODO> # Instance of Missing Data Plugin
visualization_plugin = <TODO> # Instance of Data Visualization Plugin
outlier_executor_plugin = <TODO> # Instance of Outlier Detection Executor Plugin

# -----------------
# Register Plugins with Kernel
# -----------------
kernel.add_plugin(outlier_plugin, plugin_name=<TODO>) # Register Outlier Removal Plugin
kernel.add_plugin(missing_data_plugin, plugin_name=<TODO>) # Register Missing Data Plugin
kernel.add_plugin(visualization_plugin, plugin_name=<TODO>) # Register Data Visualization Plugin
kernel.add_plugin(outlier_executor_plugin, plugin_name=<TODO>) # Register Outlier Detection Executor Plugin

# -----------------
# Create Main Orchestrator Agent with Function Calling
# -----------------
orchestrator_agent = <TODO>( # Create chat completion agent
    service=chat_service,
    name="DataAnalysisOrchestrator",
    instructions="""
    You are a Data Analysis Manager that helps users with data analysis tasks.
    
    You have access to the following specialized functions:
    - remove_outliers: For providing general guidance on removing outliers from datasets
    - handle_missing_data: For handling missing values in data
    - visualize_data: For data visualization guidance
    - clean_data_comprehensive: For comprehensive data cleaning guidance
    - execute_outlier_removal: For ACTUALLY removing outliers from numerical data provided by the user
    
    Instructions:
    1. When users provide ACTUAL numerical data (like [1,2,3,4,5]) and ask to remove outliers, use execute_outlier_removal
    2. When users ask about outlier removal methods in general (without providing data), use remove_outliers
    3. When users ask about missing data or filling missing values, use handle_missing_data  
    4. When users ask about data visualization or plotting, use visualize_data
    5. When users ask about general data cleaning, use clean_data_comprehensive
    6. For requests outside these areas, politely inform the user that you specialize in data cleaning and visualization
    
    IMPORTANT: If you see actual numbers in brackets like [1,2,3] or lists of numbers and the user mentions outliers, 
    always use execute_outlier_removal to process the actual data, not just provide general guidance.
    
    Always call the appropriate function to get specialized guidance rather than providing generic answers.
    
    When responding, mention which specialized function was used to process their request.
    """,
    kernel=<TODO> # Associate the kernel with the agent
)

# -----------------
# Main
# -----------------
async def main():
    prompts = [
        "Remove outliers from this data: [1, 100, 6]",
        "How do I remove outliers from my dataset?", 
        "How do I fill missing values in my data?",
        "How do I visualize my data?",
        "Fill in missing data from this dataset: [1, 2, None, 4, 5, None, 7]",
        "Remove outliers from this data: [1, 2, 3, 4, 5, 100, 6, 7, 8, 9]",
        "Please remove outliers from [10, 12, 11, 13, 14, 20, 15, 16, 17, 18, 300]",
        "How do I do descriptive statistics on my data?",
        "Find and remove outliers: 5, 6, 7, 8, 9, 150, 10, 11, 12"
    ]

    print("=" * 80)
    print(" Data Analysis Agent System with Semantic Kernel Functions")
    print("=" * 80)
    print(" Available Functions:")
    print("   • remove_outliers - General outlier removal guidance")
    print("   • execute_outlier_removal - Process actual numerical data")
    print("   • handle_missing_data - Missing data handling")
    print("   • visualize_data - Data visualization guidance")
    print("   • clean_data_comprehensive - Comprehensive cleaning")
    print("=" * 80)

    for index, prompt in enumerate(prompts):
        print(f"\n{'-' * 60}")
        print(f"Query {index+1}: {prompt}")
        print(f"{'-' * 60}")
        
        try:
            # Get response from orchestrator agent with function calling
            response_messages = []
            
            print(" Agent Processing...")
            async for message in orchestrator_agent.<TODO>(prompt): # Invoke the agent
                response_messages.append(str(message))
            
            full_response = " ".join(response_messages) if response_messages else "No response received"
            print(f" Agent Response: {full_response}")
            
        except Exception as e:
            print(f" Error processing query: {e}")
            
        print()  # Add spacing between queries

if __name__ == "__main__":
    asyncio.run(main())