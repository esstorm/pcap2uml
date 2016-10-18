
defaul_cap_filter = "sip||sccp||diameter"
default_uml_file="./out.uml"

# define your known UML participants here
# key can be:
# - ip address (for SIP & Diameter)
# - SCCP GT (global title) for MAP & CAMEL
# it is allowed to define multiple keys (even IP & GT) pointing to the same
# node
# !!! it doesn't matter order of definition
# this list is unordered
participants ={
    '1.1.1.1':'TAS'
    ,'2.2.2.2':'CSCF'
# for example, one logical DRA has two instances
    ,'3.3.3.3':'DRA'
    ,'4.4.4.4':'DRA'
# GT
    ,'79111111111':'MSS'
    ,'79222222222':'OCS'
    ,'79333333333':'HLR'
# TAS GT in addition to it's IP
    ,'79444444444':'TAS'
    }

# here you define the same set of participants
# but order of declaration is important
# the only name of participant has a matter, other parameters are just for
# decoration purpose
uml_intro ="""
@startuml
hide unlinked

participant "UE-A" as 1.2.1.2

participant "UE-B" as 1.2.1.3

participant "CSCF \\n 2.2.2.2" as CSCF
participant "DRA" as DRA

participant "TAS \\n 4.4.4.4 \\n 7944444444" as TAS

participant "OCS \\n 79222222222" as OCS

participant "HLR" as HLR

autonumber "<b>[000]"

"""
# you can define your own UML style

# FOR SIP ONLY
# If callid index exceed list size, then color rules will be reused from begining
colors = [
          'red'
          ,'blue'
          ,'green'
          ,'black'
          ,'aqua'
          ,'Brown'
          ,'Coral'
          ,'Magenta'
          ]
# FOR SIP ONLY
styles_callids = [ "-[#{color}]>".format(color=colors[i]) for i in range(0,len(colors)-1)]

# FOR OTHER PROTO
uml_msg_color = {
             "diameter":"black"
             ,"gsm_map":"black"
             ,"camel":"black"
             }

uml_line_style = {
              "diameter":"-[#black]>"
              ,"gsm_map":"-[#black]>"
              ,"camel":"-[#black]>"
              }

# UML Draw templates
# headers that is used here must be defined in headers dict below
proto_formatter = {
    "camel": {
              "request": "{src} {line} {dst} : <color {color}> {local} {serviceKey} \\n {isup_calling} \\n {isup_called} \n \n"
              }

    ,"gsm_map": {
                 "request": "{src} {line} {dst} : <color {color}> {gsm_old_localValue} {gsm_old_routingInfo} \n \n"
                }
    ,"sip": {
            "INVITE" : "{src} {line} {dst} : <color {color}> {request_line} {status_line} \\n from: {from_user} \\n to: {to_user} \\n callid: {call_id} \\n {sdp}  \n \n"
            ,"reINVITE" : "{src} {line} {dst} : <color {color}> re-INIVITE \\n callid: {call_id} \\n {sdp}  \n \n"
            ,"REFER" : "{src} {line} {dst} : <color {color}> {request_line} {status_line} \\n from: {from_user} \\n to: {to_user} \\n refer-to: {refer_to:.40} \\n referred-by: {referred_by} \\n callid: {call_id} \n \n"
            ,"MESSAGE": "{src} {line} {dst} : <color {color}> {method} {status_line} \\n to: {to_user} \\n callid: {call_id} \\n {content_type} \\n {gsm_a_rp_msg_type} \\n gsm da: {gsm_sms_tp_da} \\n {gsm_sms_tp_mti}  \n \n"
            ,"INFO": "{src} {line} {dst} : <color {color}> {method} {status_line} \\n callid: {call_id} \\n {content_type} \n \n"
            ,"request": "{src} {line} {dst} : <color {color}> {method} {status_line} \\n callid: {call_id} \\n {sdp}  \n \n"
            ,"short" : "{src} {line} {dst} : <color {color}> {method} {status_line} \n \n"
            }
    ,"diameter": {
            "request": "{src} {line} {dst} : <color {color}> {cmd_code} \n \n"
            ,"Command Code: 308 Subscribe-Notifications":
                "{src} {line} {dst} : <color {color}> {cmd_code} \\n {data_reference} \\n {subs_req_type} \\n {send_data_indication} \\n {3gpp_service_ind} \n \n"
            ,"Command Code: 306 User-Data":
                "{src} {line} {dst} : <color {color}> {cmd_code} \\n {data_reference} \\n {3gpp_service_ind} \n \n"
            ,"response": "{src} {line} {dst} : <color {color}> {result_code} {experimental_result_code} \n \n"
            }
    }

uml_draw_keys = ['local','gsm_old_localValue','method','cmd_code']

proto_msg_skip = {"sip": {
                          "method" : ['PRACK', 'ACK']
                          ,"status_code" : ['100','180','183']
                          }
                  ,"diameter" : {
                                 "cmd_code": ['280']
                                 }
                  }


sdp_media_attrs = ['sendrecv','sendonly','recvonly','inactive']

# headers per each protocol that will be extracted
headers = {
           "camel": { "long" : ['local','serviceKey','isup_called','isup_calling'] }

           ,"gsm_map": { "long" : ['gsm_old_localValue','gsm_old_routingInfo'] }

            ,"sip": { "short":
                           [ 'request_line', 'status_line', 'method', 'cseq_method', 'cseq',
                           'status_code', 'from_user', 'to_user', 'refer_to', 'refered_by',
                           'content_length', 'content_type','call_id',
                           # MESSAGE parameters
                           'gsm_sms_tp_da']

                        # MESSAGE parameters with description
                        ,"long" : ['gsm_sms_tp_mti', 'gsm_a_rp_msg_type']
                        }
           ,"sdp": { "short" :
                                    [ 'sdp_connection_info_address', 'sdp_session_attr',
                                      'sdp_media_attr', 'sdp_media']
                          }
           ,"diameter": {
                        "long":
                                ['auth_application_id','cmd_code','user_authorization_type','experimental_result_code','result_code','data_reference','subs_req_type','send_data_indication','3gpp_service_ind']
                        ,"short":
                                ['flags_request']
                        }
    }
