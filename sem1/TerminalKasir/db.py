import os
import json
from enum import Enum

def bubble_sort(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]

class database_type(Enum):
    STRING = 0
    INT = 1

class DatabaseError(Exception):
    """Define custom error untuk masalah database ini."""
    def __init__(self, message):
        super().__init__(message)

class table_method():
    # Kita membuat ini hanya sebagai define method saja.
    def select(self, name_key: str | list[str] | tuple[str] = "*") -> dict: pass
    def insert(self, key: list[str], value: list[any]): pass
    def delete(self, list_row: list[int] | int): pass
    def modify(self, row_index: int, keys: list[str], values: list[any]): pass

class database():
    # Private property
    __is_changed: list = [False] # Kenapa dibikin list? karena agar value ini bisa di ganti di class lain.
    __file: str = None
    __temp_data: dict = None
    __ignore_exception: bool = False
    __auto_save: bool = False

    # Private Methods
    def __save_file(self):
        open(self.__file, "w").write(json.dumps(self.__temp_data))

    def __init_table_class(self, table_name):
        class result():
            # Private Property
            __is_changed: list = None
            __table_object: dict = None
            __ignore_exception: bool = None
            __save_file: any = None

            # Methods
            def select(self, name_key: str | list | tuple = "*"):
                result: dict = {}

                # Trigger error
                if name_key == "":
                    if not self.__ignore_exception: raise DatabaseError("Name key cannot be empty.")
                    else: return {
                        "code": -1,
                        "description": "Name key cannot be empty."
                    }
                if name_key == "*":
                    result = self.__table_object["data"].copy()
                elif type(name_key) == str:
                    found = 0
                    for keys in self.__table_object["data"].keys():
                        if keys == name_key:
                            result[keys] = self.__table_object["data"][keys].copy()
                            found = 1
                            break
                    if found == 0:
                        if not self.__ignore_exception: raise DatabaseError("key named '" + name_key + "' is not exist.")
                        else: return {
                            "code": -1,
                            "description": "key named '" + name_key + "' is not exist."
                        }
                elif type(name_key) == list or type(name_key) == tuple:
                    for input_key in name_key:
                        found = 0
                        for keys in self.__table_object["data"].keys():
                            if keys == input_key:
                                result[keys] = self.__table_object["data"][keys].copy()
                                found = 1
                                break
                        if found == 0: # Jika key nya tidak found, maka trigger error
                            if not self.__ignore_exception: raise DatabaseError("key named '" + input_key + "' is not exist.")
                            else: return {
                                "code": -1,
                                "description": "key named '" + input_key + "' is not exist."
                            }
                else:
                    if not self.__ignore_exception: raise DatabaseError("Data type input of name_key is incorrect.")
                    else: return {
                        "code": -1,
                        "description": "Data type input of name_key is incorrect."
                    }

                return result
            
            def insert(self, keys_user_input: list, values_user_input: list):
                """
                Memasukkan value ke dalam table.

                Contoh code
                ```
                table = database.use_table("hello_world")
                table.insert([keys], [value])
                ```
                """
                
                if len(keys_user_input) != len(values_user_input):
                    if not self.__ignore_exception: raise DatabaseError("Total of keys array must be same with Total of value array.")
                    else: return {
                        "code": -1,
                        "description": "Total of keys array must be same with Total of value array."
                    }

                for key_input in keys_user_input:
                    if self.__table_object["data"].get(key_input) is None:
                        if not self.__ignore_exception: raise DatabaseError("key named '" + key_input + "' not found.")
                        else: return {
                            "code": -1,
                            "description": "key named '" + key_input + "' not found."
                        }

                if self.__table_object["total_column"] != len(values_user_input): # jika list value user input tidak sama dengan total column dari table tersebut, maka membuat error
                    value_len = len(values_user_input)

                    if not self.__ignore_exception: raise DatabaseError("missing " + str(self.__table_object["total_column"] - value_len) + " required list value.")
                    else: return {
                        "code": -1,
                        "description": "missing " + str(self.__table_object["total_column"] - value_len) + " required list value."
                    }

                a = 0
                result = {}
                for keys in keys_user_input:
                    key_to_index = list(self.__table_object["data"].keys()).index(keys)
                    if self.__table_object["type"][key_to_index] == database_type.STRING.value and type(values_user_input[a]) != str:
                        if not self.__ignore_exception: raise DatabaseError("Key named with '" + keys + "' must be str, not " + type(values_user_input[a]).__name__)
                        else: return {
                            "code": -1,
                            "description": "Key named with '" + keys + "' must be str, not " + type(values_user_input[a]).__name__
                        }
                    elif self.__table_object["type"][key_to_index] == database_type.INT.value and type(values_user_input[a]) != int:
                        if not self.__ignore_exception: raise DatabaseError("Key named with '" + keys + "' must be int, not " + type(values_user_input[a]).__name__)
                        else: return {
                            "code": -1,
                            "description": "Key named with '" + keys + "' must be int, not " + type(values_user_input[a]).__name__
                        }

                    self.__table_object["data"][keys].append(values_user_input[a])
                    result[keys] = values_user_input[a]
                    a = a + 1
                
                self.__table_object["total_row"] += 1
                if self.__save_file != None: self.__save_file()
                else: self.__is_changed[0] = True

            def delete(self, list_row: list[int] | int):
                if type(list_row) is list:
                    # mengurutkan angka list_row dari rendah ke tinggi (ascending) menggunakan algoritma 
                    bubble_sort(list_row)

                    for a in range(len(list_row), 0, -1):
                        for keys in self.__table_object["data"].keys():
                            if type(self.__table_object["data"][keys][list_row[a]]) is not None:
                                self.__table_object["total_row"] -= 1
                                del self.__table_object["data"][keys][list_row[a]]
                else:
                    for keys in self.__table_object["data"].keys():
                        if type(self.__table_object["data"][keys][list_row]) is not None:
                            self.__table_object["total_row"] -= 1
                            del self.__table_object["data"][keys][list_row]

            def modify(self, row_index: int, keys: list, value: list):
                a = 0 # index untuk value

                for key_input in keys:
                    # cek jika key input nya ada di table nya atau tidak
                    if self.__table_object["data"].get(key_input) is None:
                        if not self.__ignore_exception: raise DatabaseError("Key named with '" + key_input + "' is not exists.")
                        else: return {
                            "code": -1,
                            "description": "Key named with '" + key_input + "' is not exists."
                        }

                    # cek apakah row di index tersebut itu exists atau tidak
                    if self.__table_object["data"][key_input][row_index] is None:
                        if not self.__ignore_exception: raise DatabaseError("Key named with '" + key_input + "' at index " + row_index + " is not exists.")
                        else: return {
                            "code": -1,
                            "description": "Key named with '" + key_input + "' at index " + row_index + " is not exists."
                        }

                    # cek jika type input nya tidak sesuai di set table nya atau tidak
                    key_index = list(self.__table_object["data"].keys()).index(key_input)
                    if self.__table_object["type"][key_index] == database_type.INT.value and type(value[a]) != int:
                        if not self.__ignore_exception: raise DatabaseError("Key named with '" + key_input + "' must be int, not " + type(value[a]).__name__)
                        else: return {
                            "code": -1,
                            "description": "Key named with '" + key_input + "' must be int, not " + type(value[a]).__name__
                        }
                    if self.__table_object["type"][key_index] == database_type.STRING.value and type(value[a]) != str:
                        if not self.__ignore_exception: raise DatabaseError("Key named with '" + key_input + "' must be string, not " + type(value[a]).__name__)
                        else: return {
                            "code": -1,
                            "description": "Key named with '" + key_input + "' must be string, not " + type(value[a]).__name__
                        }

                    self.__table_object["data"][key_input][row_index] = value[a]
                    a = a + 1
                    
                if self.__save_file != None: self.__save_file()
                else: self.__is_changed[0] = True

            # Constructor
            def __init__(self, table_object, ignore_exception, is_changed, __save_file):
                self.__table_object = table_object
                self.__ignore_exception = ignore_exception
                self.__is_changed = is_changed
                self.__save_file = __save_file

        return result(
            self.__temp_data[table_name],
            self.__ignore_exception,
            self.__is_changed,
            self.__save_file if self.__auto_save == True else None
        )
    
    # Methods
    def load(self, name_database: str = None, ignore_exception: bool = False, auto_save: bool = False):
        if name_database == None: raise DatabaseError("Please input name database correctly.") # buat bikin error message
        
        # membuat directory
        try: os.makedirs("database")
        except: pass

        # mengeload file
        try:
            # jika file nya ada
            try:
                # jika di parsing hasil nya benar, maka dia jalankan code ini
                self.__temp_data = json.loads(open("database/" + name_database + ".json", "r").read())
            except:
                # jika tidak, maka set Object dengan tidak ada isinya
                self.__temp_data = {}
        except:
            # jika file nya tidak ada
            open("database/" + name_database + ".json", "w").write("{}")
            self.__temp_data = {}

        # mengeload JSON
        self.__file = "database/" + name_database + ".json"
        self.__ignore_exception = ignore_exception
        self.__auto_save = auto_save

        return 1
    
    def create_table(self, name_table: str, key_and_type: dict):
        """
        Create Table ini bertugas untuk membuat table.

        Contoh code nya adalah seperti ini.
        ```
        create_table("nama_table", {
            "key_string": database.STRING,
            "key_integer": database.INT
        })
        ```
        """

        if self.__temp_data.get(name_table) is not None:
            if not self.__ignore_exception: raise DatabaseError("Cannot create table named '" + name_table + "', because it's already exists.")
            else: return {
                "code": -1,
                "description": "Cannot create table named '" + name_table + "', because it's already exists."
            }
        
        # mengubah Enumerate Class menjadi angka
        for keys in key_and_type.keys():
            key_and_type[keys] = key_and_type[keys].value # dan ini akan mengeluarkan hasil dari angka enumerate tersebut.

        self.__temp_data[name_table] = {} # kita buat dulu dengan object yang kosong
        check_duplicate_key = []
        a = 0 # index untuk check_duplicate_key

        for keys_opt in key_and_type.keys():
            # check apakah ada key yang tidak di isi atau tidak
            if keys_opt == "" or keys_opt is None:
                if not self.__ignore_exception: raise DatabaseError("Cannot create table named '" + name_table + "'. because there is an empty key.")
                else: return {
                    "code": -1,
                    "description": "Cannot create table named '" + name_table + "'. becauase there is an empty key."
                }
            
            # check apakah ada duplicate key atau tidak.
            for b in range(a):
                if keys_opt == check_duplicate_key[b]:
                    if not self.__ignore_exception: raise DatabaseError("Cannot create table named '" + name_table + "'. key named '" + keys_opt + "' is already exists.")
                    else: return {
                        "code": -1,
                        "description": "Cannot create table named '" + name_table + "'. key named '" + keys_opt + "' is already exists."
                    }

            # check apakah type nya di isi atau tidak. dan apakah input type ini adalah selain int.
            if type(key_and_type[keys_opt]) != int:
                if not self.__ignore_exception: raise DatabaseError("Cannot create table named '" + name_table + "'. Type at '" + keys_opt + "' must be Enumerate or Number.")
                else: return {
                    "code": -1,
                    "description": "Cannot create table named '" + name_table + "'. Type at '" + keys_opt + "' must be Enumerate or Number."
                }
            check_duplicate_key.append(keys_opt)
            a = a + 1

        self.__temp_data[name_table]["type"] = list(key_and_type.values())
        self.__temp_data[name_table]["total_column"] = len(key_and_type)
        self.__temp_data[name_table]["total_row"] = 0
        self.__temp_data[name_table]["data"] = {}

        for keys in key_and_type.keys():
            self.__temp_data[name_table]["data"][keys] = []

        if self.__auto_save: self.__save_file()
        else: self.__is_changed[0] = True

        return 1

    def rename_table(self, old_name_table: str, new_name_table: str):
        # old name table named "name_table" is not exist
        # table named "name_table" is already exists

        if self.__temp_data.get(old_name_table) is None:
            if not self.__ignore_exception: raise DatabaseError("Cannot find old table named '" + old_name_table + "', because it's not exist.")
            else: return {
                "code": -1,
                "description": "Cannot find old table named '" + old_name_table + "', because it's not exist."
            }
        elif self.__temp_data.get(new_name_table) is not None:
            if not self.__ignore_exception: raise DatabaseError("Cannot rename table to '" + new_name_table + "', because it's already exists. try another name.")
            else: return {
                "code": -1,
                "description": "Cannot rename table to '" + new_name_table + "', because it's already exists. try another name."
            }
        
        self.__temp_data[new_name_table] = self.__temp_data[old_name_table]
        del self.__temp_data[old_name_table]

        if self.__auto_save: self.__save_file()
        else: self.__is_changed[0] = True

        return 1

    def drop_table(self, name_table: str):
        if self.__temp_data.get(name_table) is None:
            if not self.__ignore_exception: raise DatabaseError("Cannot drop table named '" + name_table + "', because table is not exist.")
            else: return {
                "code": -1,
                "description": "Cannot drop table named '" + name_table + "', because the table is not exist."
            }
        
        del self.__temp_data[name_table]

        if self.__auto_save: self.__save_file()
        else: self.__is_changed[0] = True

        return 1
    
    def info_table(self):
        """
        Mendapatkan Informasi semua table dalam database.
        """

        result = {}
        for table_name in self.__temp_data.keys():
            keys_list = {}

            for keys in self.__temp_data[table_name]["data"].keys():
                keys_list[keys] = self.__temp_data[table_name]["type"][list(self.__temp_data[table_name]["data"].keys()).index(keys)]
            
            result[table_name] = {
                table_name: {
                    "total_column": self.__temp_data[table_name]["total_column"],
                    "total_row": self.__temp_data[table_name]["total_row"],
                    "row_and_col_type": keys_list
                }
            }
            
        return result

    def use_table(self, name_table: str) -> table_method:
        for keys in self.__temp_data.keys():
            if keys == name_table:
                return self.__init_table_class(name_table)

        if not self.__ignore_exception: raise DatabaseError("Cannot use table named '" + name_table + "', because the table is not exist.")
        else: return {
            "code": -1,
            "description": "Cannot use table named '" + name_table + "', because the table is not exist."
        }

    def close(self):
        """
        Menutup database dan menyimpan database.
        """
        if self.__file == None: return {
            "code": -1,
            "description": "Database is already closed."
        }

        if self.__is_changed[0]: self.__save_file() # Save file dan close

        self.__file = None
        self.__temp_data = None

        return 1
    
    # constructor
    def __init__(self, name_database: str = "", ignore_exception: bool = False, auto_save: bool = False):
        if name_database == None: pass # jika name_database nya kosong, maka dia akan nge load secara manual
        else: self.load(name_database, ignore_exception, auto_save)

    # destructor
    def __del__(self):
        self.close()

# jika ada orang nge run file ini, maka akan muncul pesan seperti dibawah itu
# karena file ini adalah module file.
if __name__ == "__main__":
    print("This is a module file and You shouldn't run this file.\nPlease run main.py by typing 'python main.py'")