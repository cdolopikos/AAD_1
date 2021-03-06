from pickle import load
from collections import deque
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

import mldata

# df = pd.read_csv("/Users/cmdgr/OneDrive - Imperial College London/pr_data/realistic test/outvtfi0014_vvi_160_01_09_02_2021_122951_.csv")
instances=mldata.x
diagnosis = mldata.y1
treatment = mldata.y
tmp=[]
laser = 2
# todo prwta apo ola thes na fereis mesa raw data kai meta na ta kaneis preprocess


# Possible outcomes for the decison is 0 --> Noise, 1--> Normal, 2--> VVI, 3 --> AAI, 4--> VT

def getML_treatment(instance,laser):
    if laser ==1:
        # ml = load(open('svm_laser1.pkl', 'rb'))
        ml = load(open('svm_treatment_based.pkl', 'rb'))
    elif laser ==2:
        ml = load(open('svm_treatment_based.pkl', 'rb'))
    ml_based_treatment = ml.predict(instance)
    ml_based_prob = ml.predict_proba(instance)

    # print("Paok",ml_based_treatment,ml_based_prob)
    return (ml_based_treatment[0]),ml_based_prob


def getML_diagnosis(instance, laser):
    print(instance)
    if laser ==1:
        # ml = load(open('svm_laser2.pkl', 'rb'))
        ml = load(open('svm_condition_based.pkl', 'rb'))
    elif laser ==2:
        # ml = load(open('svm_laser_laser22.pkl', 'rb'))
        ml = load(open('svm_condition_based.pkl', 'rb'))
    ml_based_decision = ml.predict(instance)
    ml.partial_fit(instance, y2)
    # print(ml_based_decision[0])
    return (ml_based_decision[0])

# Checks the heamodynamic Stability of the patient based on BP estimat biomarker
# def haemodynamicStability(instance):
#     mark= instance["BP Estimat"]
#     if mark >0:
#         stability = 1
#     else:
#         stability = 0
#     return stability
#
#
# def makeDecision(ml_decision, heam_stab, ecg_based):
#     decision="n/a"
#     if ml_decision == 0 or ml_decision == 1:
#         decision = 0
#     elif ml_decision==2 or ml_decision == 3 or ml_decision==4:
#         if heam_stab==1:
#             decision=1
#         else:
#             if ecg_based == 1:
#                 decision = 1
#             else:
#                 decision = 0
#     return decision
#
# ecg_history=deque(maxlen=36)
# def ecgBased(instance):
#     bpm=instance["BPM"]
#     rr_interval = instance["R-R Interval RV"]
#     # ecg_quality=instance["EGM Quality"]
#     # current = [bpm, rr_interval, ecg_quality]
#     # ecg_history.append(current)
#     if bpm > rr_interval/10:
#         situation = 1
#     else:
#         situation =0
#     # situation=1
#     ecg_history.append(situation)
#     death_score = sum(1 for i in ecg_history if i >0)
#     if death_score > 28:
#         decision = 1
#     else:
#         decision = 0
#     return decision

ct=0
sc = StandardScaler()
final_treat=""
ml_treat=0
ml_prob=0
for i in range(len(instances)):
    X=(np.array(instances.iloc[i]).reshape(1,-1))
    bpd = X[0][7]
    # # print(X.shape)
    # # print(X[0][7])
    # # ml_dec=getML_decision(np.array(instances.iloc[i]).reshape(1,-1))
    # ml_diag=getML_diagnosis(X,laser)
    # # print(ml_diag)
    # # print(ml_treat, ml_prob)
    # if ml_diag == 3 or ml_diag==4 or ml_diag==2 or ml_diag==5:
    # print("Hooray")
    ml_treat, ml_prob=getML_treatment(X,laser)
    # final_treat=ml_treat
    if ml_treat == "Shock" and bpd>0:
        # print("nai")
        final_treat="Shock"
    elif ml_treat == "No Shock" and bpd<0:
        final_treat = "No Shock"
    elif ml_treat == "Shock" and bpd<0:
        print(ml_prob[0][1], "xyn")
        # bpd = 1.6 * bpd

        prob=ml_prob[0][1]*-1
        if abs(prob) > 0.8:
            prob=prob*2
        else:
            prob=prob*1.5
        tmp_treat = bpd + prob
        if tmp_treat<0:
            final_treat="Shock"
        else:
            final_treat="No Shock"
    elif ml_treat == "No Shock" and bpd>0:
        # bpd = 1.3 * bpd
        if abs(bpd) > 1.5:
            bpd = 2.5*bpd
        # an to bpd einai poli egalitero tou 1 tote akou to gamidid to bpd
        prob = ml_prob[0][0]*2
        tmp_treat = bpd + prob
        if tmp_treat<0:
            final_treat="Shock"
        else:
            final_treat= "No Shock"

        # print(ml_prob[0][0], "floki")
        # print(ml_prob[0], "floki")
    # print(treatment[i], final_treat)
    else:
        final_treat="No Shock"
    if treatment[i] == final_treat:
        ct +=1
    else:
        tmp.append([ml_prob,ml_treat, final_treat, bpd, treatment[i]])
        print(tmp)
    print(ct / len(treatment))

dt=pd.DataFrame(tmp)
dt.to_csv("/Users/cmdgr/OneDrive - Imperial College London/pr_data/tmp.csv")
    # print(tmp)
#     print(ml_dec," ", diagnosis[i])
#     if diagnosis[i] == ml_dec:
#         ct+=1
# print(ct/len(instances))
#     heam_stab=haemodynamicStability(instances.iloc[i])
#     ecg_based= ecgBased(instances.iloc[i])
#     final_decision=makeDecision(ml_dec, heam_stab, ecg_based)
#     if diagnosis.iloc[i]== 4 or diagnosis.iloc[i]==2 or diagnosis.iloc[i]==3:
#         if ml_dec == 1 or ml_dec==0:
#             ct=ct+1
#             print("!!!!!!!!!!!!!!!!", "diagnosis", diagnosis.iloc[i], "ml dec", ml_dec, "stab", heam_stab,"Ecg Based", ecg_based,"shock", final_decision, ct,
#                   len(diagnosis))
#
#     print("diagnosis", diagnosis.iloc[i], "ml dec", ml_dec, "stab", heam_stab,"Ecg Based", ecg_based, "shock", final_decision, ct, len(diagnosis))
#
# ml = load(open('svm.pkl', 'rb'))
# count=0
# for i in range(len(instances)):
#     x=np.array(instances.iloc[i]).reshape((1,-1))
#
#     pred=ml.predict(x)
#     if pred==diagnosis.iloc[i]:
#         count=count+1
# print(count/len(diagnosis))
# print(len(ecg_history))