import os
import os
os.environ['GOOGLE_AI_API_KEY'] = ''
import re
import json
import google.generativeai as genai
import ast
import subprocess

class CodeAssistant:
    def __init__(self, api_key):
        """Initialize Gemini-based code generation and debugging system"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_code(self, user_prompt):
        """Generate code using advanced prompt engineering"""
        system_prompt = """
        You are an expert code generation AI:
        - Provide clean, efficient, and idiomatic code
        - Include necessary imports
        - Follow best practices
        - Optimize for readability and performance
        - Explain key design choices
        """
        
        full_prompt = f"{system_prompt}\n\nUser Request: {user_prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def debug_code(self, code):
        """
        Comprehensive code debugging
        
        Args:
            code (str): Code to debug
        
        Returns:
            Debugging report
        """
        debug_report = {
            'syntax_errors': [],
            'logical_errors': [],
            'suggestions': []
        }
        
        # Syntax checking
        try:
            ast.parse(code)
        except SyntaxError as e:
            debug_report['syntax_errors'].append(str(e))
        
        # Static analysis prompt
        analysis_prompt = f"""
        Perform detailed static code analysis:
        ```python
        {code}
        ```
        
        Provide:
        - Potential performance improvements
        - Code style suggestions
        - Potential logical bugs or anti-patterns
        - Recommended best practices
        """
        
        try:
            analysis_response = self.model.generate_content(analysis_prompt)
            debug_report['suggestions'] = analysis_response.text.split('\n')
        except Exception as e:
            debug_report['logical_errors'].append(str(e))
        
        return debug_report
    
    def process_request(self, user_prompt):
        """
        End-to-end code generation and debugging
        
        Args:
            user_prompt (str): User's code generation request
        
        Returns:
            Dict with generated code and debugging report
        """
        # Generate code
        generated_code = self.generate_code(user_prompt)
        
        # Debug code
        debug_report = self.debug_code(generated_code)
        
        return {
            'code': generated_code,
            'debug_report': debug_report
        }

def main():
    # Initialize with Google AI API key
    api_key = os.getenv('GOOGLE_AI_API_KEY', '')
    assistant = CodeAssistant(api_key)
    
    # Example usage
    user_prompt = "write  an program for user madiha which is our customer she wants to order the best desert available in javascript"
    result = assistant.process_request(user_prompt)
    
    print("Generated Code:")
    print(result['code'])
    
    print("\nDebugging Report:")
    print(json.dumps(result['debug_report'], indent=2))

if __name__ == "__main__":
    main()


