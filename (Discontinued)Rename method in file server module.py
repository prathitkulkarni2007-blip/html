  var fs = require('fs');

  //Rename the file "myfile1.txt" into 
  "myrenamedfile.txt":
  fs.rename('file.txt', 'myrenamedfile.txt', function
  (err) {
    if (err) throw err;
    console.log('File Renamed!');
  });