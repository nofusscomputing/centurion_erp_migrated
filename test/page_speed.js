import { SharedArray } from 'k6/data';
import { scenario } from 'k6/execution';
import http from 'k6/http';

import { group } from 'k6';

const data = new SharedArray('urls_list', function () {
  return JSON.parse(open('parameterizedData.json')).urls_list
});



const BASE_URL = String(__ENV.BASE_URL) + '/api/v2';
const AUTH_TOKEN = __ENV.AUTH_TOKEN


const iterations = Number(100)


export const options = {

  insecureSkipTLSVerify: true,


  scenarios: {
    'page_speed': {
      executor: 'shared-iterations',
      vus: 1,
      iterations: Number(data.length * iterations),
      maxDuration: '1h',
    },
  },

  thresholds: {
    http_req_duration: [
      'p(99)<600',
      'p(95)<400',
      'p(90)<200'

    ], // 95% of requests should be below 200ms
  },

};


var COMMON_REQUEST_HEADERS = {
  dnt: '1',
  'user-agent': 'Mozilla/5.0',
  'content-type': 'application/json',
  accept: 'application/json',
  origin: BASE_URL,
  referer: BASE_URL,
  Authorization: `Token ${AUTH_TOKEN}`

};



export default function () {


  let current_iteration = Number(((scenario.iterationInTest + iterations) - ((scenario.iterationInTest + iterations) % iterations)) / iterations) - 1


  const urls = data[Number(current_iteration)];

  console.log(`arr val is: ${current_iteration} with base: ${BASE_URL} path: ${urls}`)


  const jar = http.cookieJar();
  
  const cookies = jar.cookiesForURL(`${BASE_URL}`);




  group('endpoints', function () {

    let res = http.get(`${BASE_URL}${urls}`, 
      {
        headers: COMMON_REQUEST_HEADERS,
        jar: jar,
      }
    );

  })


}
