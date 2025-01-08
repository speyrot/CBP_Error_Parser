import pandas as pd
from typing import Dict, Any

class Matcher:
    @staticmethod
    def match_records(error_df: pd.DataFrame, import_df: pd.DataFrame) -> pd.DataFrame:
        """
        Match error records with import records based on key fields
        
        Args:
            error_df (pd.DataFrame): DataFrame containing error records
            import_df (pd.DataFrame): DataFrame containing import records
            
        Returns:
            pd.DataFrame: DataFrame containing matched records with error details
            
        Raises:
            ValueError: If no matches are found
        """
        # Ensure all matching columns are strings for consistent comparison
        for df in [error_df, import_df]:
            df['Filer Code'] = df['Filer Code'].astype(str)
            df['Entry Number'] = df['Entry Number'].astype(str)
            df['7501 Line Number'] = df['7501 Line Number'].astype(str)
        
        # Perform the merge
        merged_df = pd.merge(
            error_df,
            import_df,
            on=['Filer Code', 'Entry Number', '7501 Line Number'],
            how='inner'
        )
        
        if merged_df.empty:
            raise ValueError("No matching records found between error data and import records")
        
        return merged_df

    @staticmethod
    def format_output(matched_df: pd.DataFrame) -> pd.DataFrame:
        """
        Format the matched records for output
        
        Args:
            matched_df (pd.DataFrame): DataFrame containing matched records
            
        Returns:
            pd.DataFrame: Formatted DataFrame ready for export
        """
        # Reorder columns to put error information first
        error_cols = ['Error Description', 'Filer Code', 'Entry Number', '7501 Line Number']
        other_cols = [col for col in matched_df.columns if col not in error_cols]
        
        return matched_df[error_cols + other_cols]
