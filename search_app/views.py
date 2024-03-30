from django.shortcuts import render
from .forms import SearchForm
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, "abc.xlsx")

def question(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            
            try:
                # Read Excel file into a DataFrame
                df = pd.read_excel(EXCEL_PATH)
                
                # Filter rows based on the search query
                filtered_df = df[df['question'].str.contains(search_query, case=False)]
                
                # Convert the filtered DataFrame to a list of dictionaries
                faqs = filtered_df.to_dict('records')
                
                if not faqs:
                    return render(request, 'question.html', {'form': form, 'message': 'No matching FAQs found.'})
                
                return render(request, 'question.html', {'form': form, 'faqs': faqs})
            
            except Exception as e:
                error_message = f"An error occurred: {e}"
                return render(request, 'question.html', {'form': form, 'error_message': error_message})
        
        # If form is not valid, render the form with errors
        return render(request, 'question.html', {'form': form})

    # If request method is not GET, render the form
    form = SearchForm()
    return render(request, 'question.html', {'form': form})