import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 10,             // virtual users
  duration: '1m',      // test duration
};

export default function () {
  http.get('http://localhost:8080');
  sleep(0.5);          // simulate a delay between requests
}
