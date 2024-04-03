from django.shortcuts import render
from .forms import SearchForm
import pandas as pd
import os
from django.http import JsonResponse


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
                
                # Split the answer by points and replace newline characters with <br> tags
                for faq in faqs:
                    faq['answer'] = '*'.join(faq['answer'].split('* '))

                    if 'https://' in faq['reference']:
                        parts = faq['reference'].split(' ')
                        faq['reference_label'] = ' '.join(parts[:-1])
                        faq['reference_link'] = parts[-1]
                    else:
                        faq['reference_label'] = faq['reference']
                        faq['reference_link'] = None
                
                
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


def autocomplete(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        search_term = request.GET.get('term', None)
        
        if search_term:
            try:
                df = pd.read_excel(EXCEL_PATH)
                filtered_df = df[df['question'].str.contains(search_term, case=False)]
                suggestions = filtered_df['question'].tolist()
                
                # Remove duplicates from suggestions
                suggestions = list(set(suggestions))
                
                return JsonResponse(suggestions, safe=False)
            
            except Exception as e:
                return JsonResponse({"error": str(e)})
    
    return JsonResponse({"error": "Invalid request"})

