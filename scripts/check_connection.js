const http = require('http');

http.get('http://localhost:3000/', (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    console.log('✅ Connection Successful! Received data start:');
    console.log(data.substring(0, 300) + '...'); // 응답의 앞부분만 출력
    process.exit(0);
  });
}).on('error', (err) => {
  console.error('❌ Connection Error: ' + err.message);
  process.exit(1);
});