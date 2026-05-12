  var fs = require('fs');

  //create an empty file named mynewfile2.txt:
  fs.open('mynewfile.txt', 'w', function (err, file) {
      if (err) throw err;
      console.log('File created!');
  });