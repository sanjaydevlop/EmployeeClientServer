from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'age','email' ,'contact', 'department', 'is_manager', 'manager')
    
    def clean(self):
        cleaned_data = super().clean()

        is_manager = cleaned_data.get('is_manager')
        manager = cleaned_data.get('manager')
        department=cleaned_data.get('department')
        id=cleaned_data.get('id')
        if is_manager and manager:
            raise forms.ValidationError('Managers cannot have managers.')
        # if not is_manager:
        #     Employee.department=Employee.manager.department
    
        if not is_manager and manager:
            if department != manager.department:
                raise forms.ValidationError('Non-managers must belong to the same department as their manager.')
            # if id==manager.id:
            #     raise forms.ValidationError('Self Managing is not allowed')
        if not is_manager and not manager:
            raise forms.ValidationError("Employee must have atleast one Manager or Employee must be the Manager")
        
        # if is_manager:
        #     raise forms.ValidationError("Self manager is not allowed")

        if not is_manager and id==manager.id:
            raise forms.ValidationError("Both of them have Same IDs")