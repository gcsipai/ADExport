# -*- coding: utf-8 -*-
# ADExport v2.1
# Készítette: Gcsipai, 2025

import csv
import socket
import ssl
import customtkinter as ctk
from tkinter import filedialog, messagebox
from ldap3 import Server, Connection, SUBTREE, ALL, BASE, Tls
from ldap3.core.exceptions import LDAPException

# --- NYELVI TÁMOGATÁS ---

LANGUAGES = {
    'hu': {
        'title': "ADExport v2.1 (Készítette: Gcsipai 2025)",
        'conn_settings': "Kapcsolati beállítások",
        'dc_host': "DC IP/Host:",
        'port': "Port:",
        'base_dn': "Base DN:",
        'bind_user': "Bind DN (olvasó felhasználó):",
        'password': "Jelszó:",
        'ssl_tls': "SSL/TLS használata",
        'filter_options': "Exportálási szűrők és opciók",
        'objects': "Exportálandó objektumok:",
        'users_ous': "Felhasználók és OU-k",
        'groups_members': "Csoportok és tagok",
        'user_filter': "Felhasználói állapot szűrő:",
        'filter_all': "Összes",
        'filter_enabled': "Engedélyezett",
        'filter_disabled': "Letiltott",
        'start_export': "Exportálás indítása",
        'status_ready': "Készen áll. Adja meg a kapcsolati adatokat.",
        'status_local_dc_ok': "Helyi DC és Base DN ({base_dn}) automatikusan felismerve.",
        'status_local_dc_err': "Helyi DC felismerve, de a Base DN lekérése sikertelen: {error_msg}",
        'status_connecting': "Kapcsolódás a(z) {ip}:{port} szerverhez{ssl}...",
        'status_connected': "Sikeres kapcsolat. Adatok lekérése...",
        'status_export_complete': "Exportálás befejezve.",
        'status_error': "Hiba történt az exportálás során.",
        'status_exporting_users': "Felhasználók ({filter_type}) és OU-k exportálása...",
        'status_exporting_groups': "Csoportok és tagok exportálása...",
        'status_saving_to_file': "Adatok mentése a(z) {filename} fájlba...",
        'msg_fill_all_fields': "Kérjük, töltse ki az összes kötelező kapcsolati mezőt!",
        'msg_invalid_port': "A megadott portszám érvénytelen. Kérjük, számot adjon meg.",
        'msg_conn_error_title': "Kapcsolódási hiba",
        'msg_conn_error_ldap': "LDAP hiba: {error}",
        'msg_conn_error_generic': "Általános kapcsolódási hiba: {error}",
        'msg_no_selection': "Kérjük, válasszon ki legalább egy exportálandó objektumtípust!",
        'msg_save_file_title_users': "Felhasználók és OU-k CSV mentése",
        'msg_save_file_title_groups': "Csoportok és tagok CSV mentése",
        'msg_success_title': "Siker",
        'msg_export_success': "Az exportálás sikeresen befejeződött: {filename}",
        'msg_save_error_title': "Fájlmentési hiba",
        'msg_save_error_body': "Hiba történt a fájl mentése közben: {error}",
        'msg_process_error_title': "Feldolgozási hiba",
        'msg_process_error_users': "Hiba a felhasználók/OU-k feldolgozása közben: {error}",
        'msg_process_error_groups': "Hiba a csoportok feldolgozása közben: {error}",
        'msg_no_data_found_users': "A megadott szűrővel nem található felhasználó vagy OU.",
        'msg_no_data_found_groups': "Nem található exportálható csoport.",
        'language_select': "Nyelv:",
        'theme_label': "Téma:",
        'theme_switch_dark': "Sötét",
        'theme_switch_light': "Világos",
        'csv_headers_users': ['ObjektumTípus', 'Állapot', 'Név', 'Felhasználónév', 'Keresztnév', 'Vezetéknév', 'Email', 'Mobil', 'Leírás', 'Megkülönböztetett Név (DN)'],
        'csv_headers_groups': ['Csoportnév', 'Azonosító', 'Leírás', 'Megkülönböztetett Név (DN)', 'Tagok (DN)']
    },
    'en': {
        'title': "ADExport v2.1 (Created by: Gcsipai 2025)",
        'conn_settings': "Connection Settings",
        'dc_host': "DC IP/Host:",
        'port': "Port:",
        'base_dn': "Base DN:",
        'bind_user': "Bind DN (read-only user):",
        'password': "Password:",
        'ssl_tls': "Use SSL/TLS",
        'filter_options': "Export Filters and Options",
        'objects': "Objects to Export:",
        'users_ous': "Users and OUs",
        'groups_members': "Groups and Members",
        'user_filter': "User Status Filter:",
        'filter_all': "All",
        'filter_enabled': "Enabled",
        'filter_disabled': "Disabled",
        'start_export': "Start Export",
        'status_ready': "Ready. Please provide connection details.",
        'status_local_dc_ok': "Local DC and Base DN ({base_dn}) auto-detected.",
        'status_local_dc_err': "Local DC detected, but failed to get Base DN: {error_msg}",
        'status_connecting': "Connecting to {ip}:{port}{ssl}...",
        'status_connected': "Connection successful. Retrieving data...",
        'status_export_complete': "Export complete.",
        'status_error': "An error occurred during export.",
        'status_exporting_users': "Exporting Users ({filter_type}) and OUs...",
        'status_exporting_groups': "Exporting Groups and Members...",
        'status_saving_to_file': "Saving data to {filename}...",
        'msg_fill_all_fields': "Please fill in all required connection fields!",
        'msg_invalid_port': "The port number is invalid. Please enter a number.",
        'msg_conn_error_title': "Connection Error",
        'msg_conn_error_ldap': "LDAP Error: {error}",
        'msg_conn_error_generic': "Generic Connection Error: {error}",
        'msg_no_selection': "Please select at least one object type to export!",
        'msg_save_file_title_users': "Save Users and OUs CSV",
        'msg_save_file_title_groups': "Save Groups and Members CSV",
        'msg_success_title': "Success",
        'msg_export_success': "Export completed successfully: {filename}",
        'msg_save_error_title': "File Save Error",
        'msg_save_error_body': "An error occurred while saving the file: {error}",
        'msg_process_error_title': "Processing Error",
        'msg_process_error_users': "Error processing users/OUs: {error}",
        'msg_process_error_groups': "Error processing groups: {error}",
        'msg_no_data_found_users': "No users or OUs found with the specified filter.",
        'msg_no_data_found_groups': "No exportable groups found.",
        'language_select': "Language:",
        'theme_label': "Theme:",
        'theme_switch_dark': "Dark",
        'theme_switch_light': "Light",
        'csv_headers_users': ['ObjectType', 'Status', 'Name', 'Username', 'FirstName', 'LastName', 'Email', 'Mobile', 'Description', 'DistinguishedName (DN)'],
        'csv_headers_groups': ['GroupName', 'Identifier', 'Description', 'DistinguishedName (DN)', 'Members (DN)']
    }
}

# --- KONFIGURÁCIÓS ÁLLANDÓK ---
USER_ATTRIBUTES = ['sAMAccountName', 'cn', 'givenName', 'sn', 'mail', 'distinguishedName', 'description', 'mobile', 'userAccountControl']
GROUP_ATTRIBUTES = ['cn', 'sAMAccountName', 'description', 'distinguishedName', 'member']
BASE_USER_FILTER = '(&(objectClass=user)(!(objectClass=computer)))'
OU_FILTER = '(objectClass=organizationalUnit)'
GROUP_FILTER = '(objectClass=group)'
DEFAULT_LDAP_PORT = 389
DEFAULT_LDAPS_PORT = 636

# --- AD LOGIKA ---

def get_ldap_attribute_value(entry, attribute):
    """Biztonságos LDAP attribútum érték lekérdezése, üres stringet ad vissza, ha nincs érték."""
    try:
        value = entry.get(attribute, [])
        return str(value[0]) if value else ''
    except (IndexError, AttributeError, TypeError):
        return ''

def get_default_base_dn():
    """Megpróbálja automatikusan felderíteni a Base DN-t helyi szerverről."""
    conn = None
    try:
        server = Server('localhost', get_info=ALL)
        conn = Connection(server, auto_bind=True)
        # A raise_exceptions=True itt nem ideális, mert a bind hiba is kivételt dobna
        if not conn.bound:
            return None, "Anonymous bind failed."
        return server.info.other.get('defaultNamingContext', [None])[0], None
    except LDAPException as e:
        return None, str(e)
    finally:
        if conn and conn.bound:
            conn.unbind()

def ldap_connect(dc_ip, port, bind_dn, bind_password, use_ssl):
    """LDAP kapcsolat létesítése és Connection objektum visszaadása vagy hibakezelés."""
    try:
        tls_config = Tls(validate=ssl.CERT_NONE) if use_ssl else None
        server = Server(dc_ip, port=port, use_ssl=use_ssl, tls=tls_config, get_info=ALL, connect_timeout=10)
        conn = Connection(server, bind_dn, bind_password, auto_bind=True, receive_timeout=30, raise_exceptions=True)
        return conn, None
    except LDAPException as e:
        return None, LANGUAGES['hu']['msg_conn_error_ldap'].format(error=str(e))
    except Exception as e:
        return None, LANGUAGES['hu']['msg_conn_error_generic'].format(error=str(e))


def process_users_and_ous(conn, base_dn, user_filter_type, lang):
    """Felhasználók és OU-k lekérdezése és feldolgozása a többnyelvű CSV-hez."""
    T = LANGUAGES[lang]
    
    if user_filter_type == 'Enabled':
        user_filter = f'(&{BASE_USER_FILTER}(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'
    elif user_filter_type == 'Disabled':
        user_filter = f'(&{BASE_USER_FILTER}(userAccountControl:1.2.840.113556.1.4.803:=2))'
    else:
        user_filter = BASE_USER_FILTER
        
    all_data = []
    headers = T['csv_headers_users']

    conn.search(base_dn, user_filter, search_scope=SUBTREE, attributes=USER_ATTRIBUTES, paged_size=1000)
    for user in conn.entries:
        uac = int(get_ldap_attribute_value(user, 'userAccountControl') or 0)
        is_disabled = bool(uac & 2)
        all_data.append({
            headers[0]: T['users_ous'].split(' ')[0],
            headers[1]: T['filter_disabled'] if is_disabled else T['filter_enabled'],
            headers[2]: get_ldap_attribute_value(user, 'cn'),
            headers[3]: get_ldap_attribute_value(user, 'sAMAccountName'),
            headers[4]: get_ldap_attribute_value(user, 'givenName'),
            headers[5]: get_ldap_attribute_value(user, 'sn'),
            headers[6]: get_ldap_attribute_value(user, 'mail'),
            headers[7]: get_ldap_attribute_value(user, 'mobile'),
            headers[8]: get_ldap_attribute_value(user, 'description'),
            headers[9]: str(user.distinguishedName or '')
        })

    conn.search(base_dn, OU_FILTER, search_scope=SUBTREE, attributes=['ou', 'distinguishedName'], paged_size=1000)
    for ou in conn.entries:
        all_data.append({
            headers[0]: "OU", headers[1]: "",
            headers[2]: get_ldap_attribute_value(ou, 'ou'),
            headers[3]: "", headers[4]: "", headers[5]: "", headers[6]: "", headers[7]: "", headers[8]: "",
            headers[9]: str(ou.distinguishedName or '')
        })
        
    return all_data, headers

def process_groups(conn, base_dn, lang):
    """Csoportok és tagjaik lekérdezése és feldolgozása."""
    T = LANGUAGES[lang]
    conn.search(base_dn, GROUP_FILTER, search_scope=SUBTREE, attributes=GROUP_ATTRIBUTES, paged_size=500)
    
    group_data = []
    headers = T['csv_headers_groups']
    
    for group in conn.entries:
        members = group.member.values if hasattr(group, 'member') and group.member else []
        group_data.append({
            headers[0]: get_ldap_attribute_value(group, 'cn'),
            headers[1]: get_ldap_attribute_value(group, 'sAMAccountName'),
            headers[2]: get_ldap_attribute_value(group, 'description'),
            headers[3]: str(group.distinguishedName or ''),
            headers[4]: '; '.join(members)
        })
        
    return group_data, headers

def export_to_csv(filename, data, fieldnames):
    """Adatok exportálása CSV fájlba, pontos hibakezeléssel."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
        return True, None
    except IOError as e:
        return False, str(e)

# --- GRAFIKUS FELÜLET (CUSTOMTKINTER) ---

class ADExportApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_lang = 'hu'
        self.T = LANGUAGES[self.current_lang]
        self.conn = None
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.title(self.T['title'])
        self.geometry("700x680")
        self.resizable(True, True)

        self.setup_ui()
        self.initialize_state()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        top_frame.columnconfigure(2, weight=1)

        self.lang_label = ctk.CTkLabel(top_frame, text="")
        self.lang_label.grid(row=0, column=0, padx=(10, 5), sticky="w")
        
        self.lang_options = [('hu', 'Magyar'), ('en', 'English')]
        self.lang_combobox = ctk.CTkComboBox(top_frame, values=[opt[1] for opt in self.lang_options],
                                             command=self.change_language_callback, width=120, state='readonly')
        self.lang_combobox.grid(row=0, column=1, sticky="w")
        self.lang_combobox.set('Magyar')

        self.theme_label = ctk.CTkLabel(top_frame, text="")
        self.theme_label.grid(row=0, column=2, padx=(0, 5), sticky="e")
        self.theme_switch = ctk.CTkSwitch(top_frame, text="", command=self.toggle_theme)
        self.theme_switch.grid(row=0, column=3, padx=(0, 10), sticky="e")

        conn_frame = ctk.CTkFrame(main_frame)
        conn_frame.grid(row=1, column=0, pady=10, sticky="ew")
        conn_frame.grid_columnconfigure(1, weight=1)
        
        self.conn_title = ctk.CTkLabel(conn_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.conn_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")
        
        self.dc_host_label = ctk.CTkLabel(conn_frame, text="")
        self.dc_host_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.dc_ip_entry = ctk.CTkEntry(conn_frame)
        self.dc_ip_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        self.port_label = ctk.CTkLabel(conn_frame, text="")
        self.port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.port_entry = ctk.CTkEntry(conn_frame, width=120)
        self.port_entry.grid(row=2, column=1, padx=(10,5), pady=5, sticky="w")

        self.ssl_checkbox = ctk.CTkCheckBox(conn_frame, text="", command=self.toggle_ssl)
        self.ssl_checkbox.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        self.base_dn_label = ctk.CTkLabel(conn_frame, text="")
        self.base_dn_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.base_dn_entry = ctk.CTkEntry(conn_frame)
        self.base_dn_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.bind_user_label = ctk.CTkLabel(conn_frame, text="")
        self.bind_user_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.bind_dn_entry = ctk.CTkEntry(conn_frame)
        self.bind_dn_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.password_label = ctk.CTkLabel(conn_frame, text="")
        self.password_label.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="w")
        self.password_entry = ctk.CTkEntry(conn_frame, show="*")
        self.password_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=(5, 10), sticky="ew")

        options_frame = ctk.CTkFrame(main_frame)
        options_frame.grid(row=2, column=0, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        self.filter_title = ctk.CTkLabel(options_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.filter_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

        self.objects_label = ctk.CTkLabel(options_frame, text="")
        self.objects_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.export_users_var = ctk.BooleanVar(value=True)
        self.export_groups_var = ctk.BooleanVar(value=True)
        self.users_checkbox = ctk.CTkCheckBox(options_frame, variable=self.export_users_var)
        self.users_checkbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.groups_checkbox = ctk.CTkCheckBox(options_frame, variable=self.export_groups_var)
        self.groups_checkbox.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.user_filter_label = ctk.CTkLabel(options_frame, text="")
        self.user_filter_label.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="w")
        self.user_filter_combobox = ctk.CTkComboBox(options_frame, state='readonly')
        self.user_filter_combobox.grid(row=2, column=1, columnspan=2, padx=10, pady=(5, 10), sticky="ew")

        self.export_button = ctk.CTkButton(main_frame, command=self.start_export)
        self.export_button.grid(row=3, column=0, pady=20, sticky="ew")
        
        self.status_label = ctk.CTkLabel(main_frame, text="", anchor="w", fg_color="transparent")
        self.status_label.grid(row=4, column=0, sticky="ew")

    def initialize_state(self):
        base_dn, error = get_default_base_dn()
        if base_dn:
            self.dc_ip_entry.insert(0, "localhost")
            self.dc_ip_entry.configure(state="readonly")
            self.base_dn_entry.insert(0, base_dn)
            self.status_message = ('status_local_dc_ok', {'base_dn': base_dn}, "green")
        else:
            self.status_message = ('status_local_dc_err', {'error_msg': error}, "red") if error else ('status_ready', {}, "gray")
        self.port_entry.insert(0, str(DEFAULT_LDAP_PORT))
        self.update_texts()

    def update_texts(self):
        self.T = LANGUAGES[self.current_lang]
        self.title(self.T['title'])
        self.lang_label.configure(text=self.T['language_select'])
        self.theme_label.configure(text=self.T['theme_label'])
        self.conn_title.configure(text=self.T['conn_settings'])
        self.dc_host_label.configure(text=self.T['dc_host'])
        self.port_label.configure(text=self.T['port'])
        self.ssl_checkbox.configure(text=self.T['ssl_tls'])
        self.base_dn_label.configure(text=self.T['base_dn'])
        self.bind_user_label.configure(text=self.T['bind_user'])
        self.password_label.configure(text=self.T['password'])
        self.filter_title.configure(text=self.T['filter_options'])
        self.objects_label.configure(text=self.T['objects'])
        self.users_checkbox.configure(text=self.T['users_ous'])
        self.groups_checkbox.configure(text=self.T['groups_members'])
        self.user_filter_label.configure(text=self.T['user_filter'])

        filter_values = [self.T['filter_all'], self.T['filter_enabled'], self.T['filter_disabled']]
        current_selection = self.user_filter_combobox.get()
        self.user_filter_combobox.configure(values=filter_values)
        if not current_selection or current_selection not in filter_values:
            self.user_filter_combobox.set(self.T['filter_all'])
        
        self.export_button.configure(text=self.T['start_export'])
        self.update_status(*self.status_message)
        self.update_theme_switch_text()

    def update_status(self, msg_key, params={}, color="gray"):
        message = self.T.get(msg_key, "Unknown status").format(**params)
        colors = {"gray": ("#666", "#ccc"), "blue": ("#3498db", "#5dade2"), 
                  "green": ("#27ae60", "#2ecc71"), "red": ("#c0392b", "#e74c3c")}
        self.status_label.configure(text=message, text_color=colors.get(color, colors["gray"]))
        self.update_idletasks()

    def change_language_callback(self, selection):
        self.current_lang = next(code for code, name in self.lang_options if name == selection)
        self.update_texts()

    def toggle_theme(self):
        new_mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.update_theme_switch_text()

    def update_theme_switch_text(self):
        is_dark = ctk.get_appearance_mode() == "Dark"
        self.theme_switch.configure(text=self.T['theme_switch_dark'] if is_dark else self.T['theme_switch_light'])

    def toggle_ssl(self):
        port = str(DEFAULT_LDAPS_PORT) if self.ssl_checkbox.get() else str(DEFAULT_LDAP_PORT)
        self.port_entry.delete(0, 'end')
        self.port_entry.insert(0, port)
            
    def set_ui_state(self, is_enabled):
        state = "normal" if is_enabled else "disabled"
        self.export_button.configure(state=state)
        if "localhost" not in self.dc_ip_entry.get():
             self.dc_ip_entry.configure(state=state)
        self.port_entry.configure(state=state)
        self.base_dn_entry.configure(state=state)
        self.bind_dn_entry.configure(state=state)
        self.password_entry.configure(state=state)
        self.ssl_checkbox.configure(state=state)
        self.lang_combobox.configure(state=state)
        self.user_filter_combobox.configure(state=state)
        self.users_checkbox.configure(state=state)
        self.groups_checkbox.configure(state=state)
        
    def start_export(self):
        self.set_ui_state(False)
        
        try:
            port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror(self.T['msg_process_error_title'], self.T['msg_invalid_port'])
            self.set_ui_state(True)
            return

        conn_details = {
            "dc_ip": self.dc_ip_entry.get().strip(),
            "base_dn": self.base_dn_entry.get().strip(),
            "bind_dn": self.bind_dn_entry.get().strip(),
            "password": self.password_entry.get()
        }
        if not all(conn_details.values()):
            messagebox.showerror(self.T['msg_process_error_title'], self.T['msg_fill_all_fields'])
            self.set_ui_state(True)
            return
            
        if not self.export_users_var.get() and not self.export_groups_var.get():
            messagebox.showwarning(self.T['msg_process_error_title'], self.T['msg_no_selection'])
            self.set_ui_state(True)
            return

        ssl_text = " (SSL)" if self.ssl_checkbox.get() else ""
        self.update_status('status_connecting', {'ip': conn_details['dc_ip'], 'port': port, 'ssl': ssl_text}, "blue")
        self.conn, error = ldap_connect(conn_details['dc_ip'], port, conn_details['bind_dn'], conn_details['password'], self.ssl_checkbox.get())
        
        if error:
            messagebox.showerror(self.T['msg_conn_error_title'], error)
            self.update_status('status_error', {}, "red")
            self.set_ui_state(True)
            return
            
        self.update_status('status_connected', {}, "green")

        try:
            if self.export_users_var.get():
                self.run_single_export(process_users_and_ous, 'users')
            
            if self.export_groups_var.get():
                self.run_single_export(process_groups, 'groups')

            self.update_status('status_export_complete', {}, "green")
        finally:
            if self.conn and self.conn.bound:
                self.conn.unbind()
            self.set_ui_state(True)

    def run_single_export(self, process_func, export_type):
        filter_display_map = {v: k.replace('filter_', '').capitalize() for k, v in self.T.items() if k.startswith('filter_')}
        user_filter_type = filter_display_map.get(self.user_filter_combobox.get(), 'All')
        
        self.update_status(f'status_exporting_{export_type}', {'filter_type': self.user_filter_combobox.get()}, "blue")
        
        try:
            data, headers = process_func(self.conn, self.base_dn_entry.get().strip(), self.current_lang, user_filter_type) if export_type == 'users' else process_func(self.conn, self.base_dn_entry.get().strip(), self.current_lang)
            
            if not data:
                messagebox.showinfo(self.T['msg_success_title'], self.T[f'msg_no_data_found_{export_type}'])
                return
                
            filename = filedialog.asksaveasfilename(
                title=self.T[f'msg_save_file_title_{export_type}'],
                defaultextension=".csv",
                initialfile=f"ad_export_{export_type}_{user_filter_type.lower()}.csv" if export_type == 'users' else f"ad_export_{export_type}.csv",
                filetypes=[("CSV fájlok", "*.csv"), ("Minden fájl", "*.*")]
            )
            
            if not filename: return

            self.update_status('status_saving_to_file', {'filename': filename.split('/')[-1]}, "blue")
            success, error = export_to_csv(filename, data, headers)
            
            if success:
                messagebox.showinfo(self.T['msg_success_title'], self.T['msg_export_success'].format(filename=filename.split('/')[-1]))
            else:
                messagebox.showerror(self.T['msg_save_error_title'], self.T['msg_save_error_body'].format(error=error))
        except Exception as e:
            messagebox.showerror(self.T['msg_process_error_title'], self.T[f'msg_process_error_{export_type}'].format(error=str(e)))
            self.update_status('status_error', {}, "red")
        
if __name__ == "__main__":
    app = ADExportApp()
    app.mainloop()
