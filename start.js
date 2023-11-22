const cheerio = require('cheerio');
const axios = require('axios');

axios.get('http://www.xuexili.com/mayizhuangyuan/jinridaan.html').then(res => {
  const $ = cheerio.load(res.data);
  const today1 = $('div.contl').find('table').find('table').find('tr:first').next();
  const today2 = today1.next();
  const today1Date = today1.find('td:first');
  const today1Question = today1Date.next();
  const today1Answer = today1Question.next();
  const today2Date = today2.find('td:first');
  const today2Question = today2Date.next();
  const today2Answer = today2Question.next();
  const firstText = `${today1Date.text().split('年')[1].trim()}问题：${today1Question.text().trim()} 答案：${today1Answer.text().trim()}`;
  const nextText = `${today2Date.text().split('年')[1].trim()}问题：${today2Question.text().trim()} 答案：${today2Answer.text().trim()}`;
  axios.post("https://thor.emoz.top/ant/insert.php", {
    'data': [firstText, nextText]
  }).then(res => {
    console.log('插入成功', res.data);
  })
  console.log(firstText, nextText);
})