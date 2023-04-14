import requests
from requests.auth import HTTPBasicAuth
import base64
import datetime
import credentials


class MpesaBase:
    def __init__(
        self,
        env="sandbox",
        app_key=credentials.consumer_key,
        app_secret=credentials.consumer_secret,
        sandbox_url="https://sandbox.safaricom.co.ke",
        live_url="https://api.safaricom.co.ke",
    ):
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.token = None

    def authenticate(self):

        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        authenticate_uri = "/oauth/v1/generate?grant_type=client_credentials"
        authenticate_url = "{0}{1}".format(
            base_safaricom_url, authenticate_uri)
        try:
            r = requests.get(
                authenticate_url, auth=HTTPBasicAuth(
                    self.app_key, self.app_secret)
            )
        except Exception as e:
            r = requests.get(
                authenticate_url,
                auth=HTTPBasicAuth(self.app_key, self.app_secret),
                verify=False,
            )
        self.token = r.json()["access_token"]
        return r.json()["access_token"]
        print(r.json())

# class C2B(MpesaBase):
#     def __init__(
#         self,
#         env="sandbox",
#         app_key=None,
#         app_secret=None,
#         sandbox_url="https://sandbox.safaricom.co.ke",
#         live_url="https://api.safaricom.co.ke",
#     ):
#         MpesaBase.__init__(self, env, app_key, app_secret,
#                            sandbox_url, live_url)
#         self.authentication_token = self.authenticate()

#     def register(
#         self,
#         shortcode=None,
#         response_type=None,
#         confirmation_url=None,
#         validation_url=None,
#     ):

#         payload = {
#             "ShortCode": shortcode,
#             "ResponseType": response_type,
#             "ConfirmationURL": confirmation_url,
#             "ValidationURL": validation_url,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(
#             base_safaricom_url, "/mpesa/c2b/v1/registerurl")
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()

#     def simulate(
#         self,
#         shortcode=None,
#         command_id=None,
#         amount=None,
#         msisdn=None,
#         bill_ref_number=None,
#     ):

#         payload = {
#             "ShortCode": shortcode,
#             "CommandID": command_id,
#             "Amount": amount,
#             "Msisdn": msisdn,
#             "BillRefNumber": bill_ref_number,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/simulate")
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()


# class MpesaExpress(MpesaBase):
#     def __init__(
#         self,
#         env="sandbox",
#         app_key=None,
#         app_secret=None,
#         sandbox_url="https://sandbox.safaricom.co.ke",
#         live_url="https://api.safaricom.co.ke",
#     ):
#         MpesaBase.__init__(self, env, app_key, app_secret,
#                            sandbox_url, live_url)
#         self.authentication_token = self.authenticate()

#     def stk_push(
#         self,
#         business_shortcode=None,
#         passcode=None,
#         amount=None,
#         callback_url=None,
#         reference_code=None,
#         phone_number=None,
#         description=None,
#     ):

#         time = (
#             str(datetime.datetime.now())
#             .split(".")[0]
#             .replace("-", "")
#             .replace(" ", "")
#             .replace(":", "")
#         )
#         password = "{0}{1}{2}".format(
#             str(business_shortcode), str(passcode), time)
#         encoded = base64.b64encode(bytes(password, encoding="utf8"))
#         payload = {
#             "BusinessShortCode": business_shortcode,
#             "Password": encoded.decode("utf-8"),
#             "Timestamp": time,
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": amount,
#             "PartyA": int(phone_number),
#             "PartyB": business_shortcode,
#             "PhoneNumber": int(phone_number),
#             "CallBackURL": callback_url,
#             "AccountReference": reference_code,
#             "TransactionDesc": description,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(
#             base_safaricom_url, "/mpesa/stkpush/v1/processrequest"
#         )
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()

#     def query(self, business_shortcode=None, checkout_request_id=None, passcode=None):

#         time = (
#             str(datetime.datetime.now())
#             .split(".")[0]
#             .replace("-", "")
#             .replace(" ", "")
#             .replace(":", "")
#         )
#         password = "{0}{1}{2}".format(
#             str(business_shortcode), str(passcode), time)
#         encoded = base64.b64encode(bytes(password, encoding="utf8"))
#         payload = {
#             "BusinessShortCode": business_shortcode,
#             "Password": encoded.decode("utf-8"),
#             "Timestamp": time,
#             "CheckoutRequestID": checkout_request_id,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(
#             base_safaricom_url, "/mpesa/stkpushquery/v1/query")
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()


# class Reversal(MpesaBase):
#     def __init__(
#         self,
#         env="sandbox",
#         app_key=None,
#         app_secret=None,
#         sandbox_url="https://sandbox.safaricom.co.ke",
#         live_url="https://api.safaricom.co.ke",
#     ):
#         MpesaBase.__init__(self, env, app_key, app_secret,
#                            sandbox_url, live_url)
#         self.authentication_token = self.authenticate()

#     def reverse(
#         self,
#         initiator=None,
#         security_credential=None,
#         command_id="TransactionReversal",
#         transaction_id=None,
#         amount=None,
#         receiver_party=None,
#         receiver_identifier_type=None,
#         queue_timeout_url=None,
#         result_url=None,
#         remarks=None,
#         occassion=None,
#     ):

#         payload = {
#             "Initiator": initiator,
#             "SecurityCredential": security_credential,
#             "CommandID": command_id,
#             "TransactionID": transaction_id,
#             "Amount": amount,
#             "ReceiverParty": receiver_party,
#             "ReceiverIdentifierType": receiver_identifier_type,
#             "QueueTimeOutURL": queue_timeout_url,
#             "ResultURL": result_url,
#             "Remarks": remarks,
#             "Occassion": occassion,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(
#             base_safaricom_url, "/mpesa/reversal/v1/request")
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()


# class TransactionStatus(MpesaBase):
#     def __init__(
#         self,
#         env="sandbox",
#         app_key=None,
#         app_secret=None,
#         sandbox_url="https://sandbox.safaricom.co.ke",
#         live_url="https://api.safaricom.co.ke",
#     ):
#         MpesaBase.__init__(self, env, app_key, app_secret,
#                            sandbox_url, live_url)
#         self.authentication_token = self.authenticate()

#     def check_transaction_status(
#         self,
#         party_a=None,
#         identifier_type=None,
#         remarks=None,
#         initiator=None,
#         passcode=None,
#         result_url=None,
#         queue_timeout_url=None,
#         transaction_id=None,
#         occassion=None,
#         shortcode=None,
#     ):

#         time = (
#             str(datetime.datetime.now())
#             .split(".")[0]
#             .replace("-", "")
#             .replace(" ", "")
#             .replace(":", "")
#         )
#         password = "{0}{1}{2}".format(str(shortcode), str(passcode), time)
#         encoded = base64.b64encode(bytes(password, encoding="utf-8"))
#         payload = {
#             "CommandID": "TransactionStatusQuery",
#             "PartyA": party_a,
#             "IdentifierType": identifier_type,
#             "Remarks": remarks,
#             "Initiator": initiator,
#             "SecurityCredential": encoded.decode("utf-8"),
#             "QueueTimeOutURL": queue_timeout_url,
#             "ResultURL": result_url,
#             "TransactionID": transaction_id,
#             "Occasion": occassion,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(
#             base_safaricom_url, "/mpesa/stkpushquery/v1/query")
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()


# class Balance(MpesaBase):
#     def __init__(
#         self,
#         env="sandbox",
#         app_key=None,
#         app_secret=None,
#         sandbox_url="https://sandbox.safaricom.co.ke",
#         live_url="https://api.safaricom.co.ke",
#     ):
#         MpesaBase.__init__(self, env, app_key, app_secret,
#                            sandbox_url, live_url)
#         self.authentication_token = self.authenticate()

#     def get_balance(
#         self,
#         initiator=None,
#         security_credential=None,
#         command_id=None,
#         party_a=None,
#         identifier_type=None,
#         remarks=None,
#         queue_timeout_url=None,
#         result_url=None,
#     ):

#         payload = {
#             "Initiator": initiator,
#             "SecurityCredential": security_credential,
#             "CommandID": command_id,
#             "PartyA": party_a,
#             "IdentifierType": identifier_type,
#             "Remarks": remarks,
#             "QueueTimeOutURL": queue_timeout_url,
#             "ResultURL": result_url,
#         }
#         headers = {
#             "Authorization": "Bearer {0}".format(self.authentication_token),
#             "Content-Type": "application/json",
#         }
#         if self.env == "production":
#             base_safaricom_url = self.live_url
#         else:
#             base_safaricom_url = self.sandbox_url
#         saf_url = "{0}{1}".format(
#             base_safaricom_url, "/mpesa/accountbalance/v1/query")
#         try:
#             r = requests.post(saf_url, headers=headers, json=payload)
#         except Exception as e:
#             r = requests.post(saf_url, headers=headers,
#                               json=payload, verify=False)
#         return r.json()
