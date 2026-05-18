  var fs = require('fs');

  //Delete the file mynewfile2.txt:
  fs.unlink('newfile.txt', function (err){
    if (err) throw err;
    console.log('File deleted!');
  });