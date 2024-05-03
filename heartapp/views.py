from django.shortcuts import render # type: ignore
from joblib import load
import pandas as pd


model = load(r'C:\Users\sruja\OneDrive\Desktop\mldeploymemnt\savedmodels\model.joblib')

model_columns=['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak', 'Sex_F', 'Sex_M', 'ChestPainType_ASY', 'ChestPainType_ATA', 'ChestPainType_NAP',
 'ChestPainType_TA', 'RestingECG_LVH', 'RestingECG_Normal', 'RestingECG_ST', 'ExerciseAngina_N',
 'ExerciseAngina_Y', 'ST_Slope_Down', 'ST_Slope_Flat', 'ST_Slope_Up']

def predictor(request):
    return render(request,'main.html')

def forminfo(request):
    # Get form data
    age = request.GET.get('age')
    resting_bp = request.GET.get('resting_bp')
    cholesterol = request.GET.get('cholestrol')
    fasting_bs = request.GET.get('fasting_bs')
    max_hr = request.GET.get('max_hr')
    oldpeak = request.GET.get('oldpeak')
    sex = request.GET.get('Sex')
    chest_pain_type = request.GET.get('ChestPainType')
    resting_ecg = request.GET.get('RestingECG')
    exercise_angina = request.GET.get('ExerciseAngina')
    st_slope = request.GET.get('STSlope')
    
    # Initialize data dictionary with default values
    data = {col: 0 for col in model_columns}

    if sex == 'Sex_F':
        data['Sex_F'] = 1
        data['Sex_M'] = 0
    elif sex == 'Sex_M':
        data['Sex_F'] = 0
        data['Sex_M'] = 1

    if chest_pain_type == 'ChestPainType_ASY':
        data['ChestPainType_ASY'] = 1
        data['ChestPainType_ATA'] = 0
        data['ChestPainType_NAP'] = 0
        data['ChestPainType_TA'] = 0
    elif chest_pain_type == 'ChestPainType_ATA':
        data['ChestPainType_ASY'] = 0
        data['ChestPainType_ATA'] = 1
        data['ChestPainType_NAP'] = 0
        data['ChestPainType_TA'] = 0
    elif chest_pain_type == 'ChestPainType_NAP':
        data['ChestPainType_ASY'] = 0
        data['ChestPainType_ATA'] = 0
        data['ChestPainType_NAP'] = 1
        data['ChestPainType_TA'] = 0
    elif chest_pain_type == 'ChestPainType_TA':
        data['ChestPainType_ASY'] = 0
        data['ChestPainType_ATA'] = 0
        data['ChestPainType_NAP'] = 0
        data['ChestPainType_TA'] = 1

    if resting_ecg == 'RestingECG_LVH':
        data['RestingECG_LVH'] = 1
        data['RestingECG_Normal'] = 0
        data['RestingECG_ST'] = 0
    elif resting_ecg == 'RestingECG_Normal':
        data['RestingECG_LVH'] = 0
        data['RestingECG_Normal'] = 1
        data['RestingECG_ST'] = 0
    elif resting_ecg == 'RestingECG_ST':
        data['RestingECG_LVH'] = 0
        data['RestingECG_Normal'] = 0
        data['RestingECG_ST'] = 1

    if exercise_angina == 'ExerciseAngina_N':
        data['ExerciseAngina_N'] = 1
        data['ExerciseAngina_Y'] = 0
    elif exercise_angina == 'ExerciseAngina_Y':
        data['ExerciseAngina_N'] = 0
        data['ExerciseAngina_Y'] = 1

    if st_slope == 'ST_Slope_Down':
        data['ST_Slope_Down'] = 1
        data['ST_Slope_Flat'] = 0
        data['ST_Slope_Up'] = 0
    elif st_slope == 'ST_Slope_Flat':
        data['ST_Slope_Down'] = 0
        data['ST_Slope_Flat'] = 1
        data['ST_Slope_Up'] = 0
    elif st_slope == 'ST_Slope_Up':
        data['ST_Slope_Down'] = 0
        data['ST_Slope_Flat'] = 0
        data['ST_Slope_Up'] = 1

    data['Age'] = age
    data['RestingBP'] = resting_bp
    data['Cholesterol'] = cholesterol
    data['FastingBS'] = fasting_bs
    data['MaxHR'] = max_hr
    data['Oldpeak'] = oldpeak

    input_df = pd.DataFrame([data])
    pd.set_option('display.max_columns', None)

    print(input_df)  # Print the input DataFrame for further inspection

    y_pred = model.predict(input_df)
    if y_pred[0] == 1:
        y_pred = 'Disease present'
    else:
        y_pred = 'No disease present'
    return render(request, 'result.html', {'result': y_pred})
