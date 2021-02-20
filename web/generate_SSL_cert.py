from OpenSSL import crypto
import common_tools


# This sets where it will pull settings from
settings = common_tools.yaml_to_dict(common_tools.correct_path('settings/generate_SSL_cert.yaml'))


# This generates the self signed SSL certificate
def cert_gen(serialNumber=0, validityEndInSeconds=10*365*24*60*60):
    # Can look at generated file using openssl:
    # openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = settings['countryName']
    cert.get_subject().ST = settings['stateOrProvinceName']
    cert.get_subject().L = settings['localityName']
    cert.get_subject().O = settings['organizationName']
    cert.get_subject().OU = settings['organizationUnitName']
    cert.get_subject().CN = settings['commonName']
    cert.get_subject().emailAddress = settings['emailAddress']
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    CERT_FILE = settings['cert_file']
    KEY_FILE = settings['key_file']
    CERT_FILE = settings['cert_folder'] + '/' + CERT_FILE
    KEY_FILE = settings['cert_folder'] + '/' + KEY_FILE
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

if '__main__' == __name__:
    cert_gen()