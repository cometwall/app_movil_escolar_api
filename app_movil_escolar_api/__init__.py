import pymysql
pymysql.install_as_MySQLdb()
#Esta línea registra pymysql con ese alias
#  y evita errores de importación cuando se conecte a MySQL sin mysqlclient.