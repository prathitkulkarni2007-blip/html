var mysql = require("mysql");

var connection = mysql.createConnection({
    host: "remotemysql.com", // Give your host name
    user: "Rz8hqn1dk4", // Give your username
    password: "nd0wK03xe0", // Give your password
    database: "Rz8hqn1dk4" // Giver your DB name   
    });

connection.connect((err) => {
    if(err) throw err
    console.log("connected");
    var sql = "CREATE TABLE Student(Student_ID INT, Student_FirstName VARCHAR(255), Student_LastName VARCHAR(255), Student_City VARCHAR(255))";
     connection.query(sql, function(err, result) {
     if(err) throw err;
     console.log("Table created in DB");
     });
});