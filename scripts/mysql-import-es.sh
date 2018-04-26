lib=$JDBC_IMPORTER_HOME/lib/
bin=$JDBC_IMPORTER_HOME/bin/

echo '
{
    "type" : "jdbc",
    "jdbc" : {
        "url" : "jdbc:mysql://gz-cdb-ko3zdkzs.sql.tencentcdb.com:63440/test",
        "user" : "shendu",
        "password" : "P@55word",
        "sql": "select * from parent_table",
        "elasticsearch" : {
            "autodiscover" : "true",
            "cluster" : "my-application",
            "host" : "localhost",
            "port" : 9300
        },
        "index" : "myindex2",
        "type" : "myparents2"
    }
}
' | java \
    -cp "${lib}/*" \
    -Dlog4j.configurationFile=${bin}/log4j2.xml \
    org.xbib.tools.Runner \
    org.xbib.tools.JDBCImporter

# "sql" : "select \"myindex\" as _index, \"myparents\" as _type, id as _id, message from parent_table",