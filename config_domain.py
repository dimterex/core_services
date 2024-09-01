import os.path
import sys
from subprocess import Popen

SSL_CERTIFICATE_FILE_PATH = '/etc/apache2/ssl/server.crt'
SSL_CERTIFICATE_KEY_FILE_PATH = '/etc/apache2/ssl/server.key'

APACHE_DIRECTORY_CONFIG_PATH = '/etc/apache2'
# APACHE_DIRECTORY_CONFIG_PATH = 'C:\\Users\\UseR\\Downloads\\Temp deploy'


def get_template(server_name: str, proxy_pass: str) -> [str]:
    sb = []
    sb.append('<VirtualHost *: 443>')
    sb.append('\tSSLEngine On')
    sb.append('\tSSLProxyEngine On')
    sb.append(f'\tServerName {server_name}')
    sb.append(f'\tServerAlias {server_name}')

    sb.append('\tProxyPreserveHost On')
    sb.append(f'\tSSLCertificateFile "{SSL_CERTIFICATE_FILE_PATH}"')
    sb.append(f'\tSSLCertificateKeyFile "{SSL_CERTIFICATE_KEY_FILE_PATH}"')
    sb.append(f'\tProxyPass / {proxy_pass}')
    sb.append(f'\tProxyPassReverse / {proxy_pass}')
    # sb.append('\tErrorLog ${APACHE_LOG_DIR}/error.log')
    # sb.append('\tCustomLog ${APACHE_LOG_DIR}/access.log combined')
    sb.append('</VirtualHost>')

    return sb


def apply_changes(config_name: str):
    process = Popen(f'a2ensite {config_name}')
    with process.stdout:
        print(process.stdout)
    process.wait()  # 0 means success
    process = Popen(f'service apache2 restart')
    with process.stdout:
        print(process.stdout)
    process.wait()  # 0 means success

def main(args: []):
    if len(args) != 3:
        raise Exception('Cant execute. Arguments are not correctly.')

    server_name = args[1]
    if not server_name.endswith('.server'):
        raise Exception('First arg is server name, and should be ended with ".server".')

    proxy_pass = args[2]
    if not proxy_pass.endswith('/'):
        proxy_pass += '/'
    template = get_template(server_name, proxy_pass)

    with open(os.path.join(APACHE_DIRECTORY_CONFIG_PATH, server_name + '.conf'), 'w') as config:
        config.write('\n'.join(template))

    apply_changes(server_name)
    print('Done')


if __name__ == '__main__':
    main(sys.argv)
