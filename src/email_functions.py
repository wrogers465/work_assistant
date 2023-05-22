# import pyperclip
# from classes import Email, Inmate


# def monitor_email(email: Email, docket: str) -> Email:
#     inmate = Inmate(docket)
    
    
#     if len(docket) != 7 and not docket.isnumeric():
#         return None

#     monitor_types = {'CAM': ['CAM', 'ALCOHOL MONITOR'],
#                         'GPS': ['GPS', 'ELECTRONIC MONITOR'],
#                         'RBT': ['RBT', 'REMOTE BREATH']}

#     release_types = {'S/ROR': ['S/ROR', 'SUPERVISED ROR', 'SROR'],
#                         'ROR': ['ROR', 'U/ROR', 'UNSUPERVISED ROR'],
#                         'Bond': ['BOND REMAIN', 'BOND AMENDED'],
#                         'EMP Transfer': ['SERVED ON GPS',
#                                         'TO BE SERVED ON ALTERNATIVE SENTENCING'],
#                         'Prob': ['PROBATION']}


#     court_minutes = pyperclip.paste()
#     release_type = court_minutes.find_match(release_types, end_fast=True)
#     monitors = court_minutes.find_match(monitor_types)

#     body_flag = 'Please advise when to schedule.'
    
#     try:
#         subject = f'{release_type[0]}'
#     except IndexError as e:
#         return e
    
#     if 'EMP Transfer' in release_type:
#         try:
#             monitors.remove('GPS')
#         except ValueError:
#             pass            

    
#     inmate = Inmate(docket)



#     match len(monitors):
#         case 1:
#             subject += f' w/ {monitors[0]}'
#         case 2:
#             subject += f' w/ {monitors[0]} & {monitors[1]}'
#         case default:
#             pass


    # if baker_act_var == 1:
        
    #     def get_pronouns(gender):
    #         return {'MALE': ('He', 'his'),
    #                         'FEMALE': ('She', 'her')}.get(gender, ('He', 'his'))

    #     def get_phrasing(release_type):
    #         match release_type:
    #             case 'Bond':
    #                 return f'has posted {release_type.lower()} and a monitor is a condition of release'
    #             case default:
    #                 return f'was given {release_type} today in court and a monitor is a condition of release'

    #     pronouns = get_pronouns(inmate.gender)
    #     phrasing_1 = get_phrasing(release_type[0])
        
    #     subject += ' (To PEMHS)'
    #     body_flag = f'''The above subject {phrasing_1}. {pronouns[0]} is also being baker acted and will be transported to PEMHS.

    #                             If needed, we can provide PEMHS a hold order instructing that ASU/APAD be called prior to {pronouns[1]} discharge.'''
        
    # subject += f' - {inmate.short_lname}'


    # body = f'''Docket: {inmate.docket}
    #             Name: {inmate.name}
    #             Person ID: {inmate.person_id}
                

    #             {body_flag}


    #             Thanks,


    #             {court_minutes.text}'''


    # email = Email(subject, body, to='ASU + MPU', cc='SSs + COC')
    # return email

def Peso(email_data: dict) -> dict:
    print("hello")
    return email_data