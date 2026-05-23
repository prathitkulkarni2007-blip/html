var mysql = require('mysql');

var con = mysql.createConnection({
    host: "remotemySql.com", // Give your host name
    user: "Rz8hqn1dK4", // Give your username
    password: "nd0wKO3xe0", // Give your password
});

con.connect(function(err) {
    if (err) throw err;
    console.log("Connected!");
});