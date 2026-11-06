// k6 run loadtest/salary-day.js   (Project 2: simulate the 25th-of-the-month spike)
import http from "k6/http";
import { check, sleep } from "k6";
export const options = {
  stages: [ { duration: "1m", target: 20 }, { duration: "3m", target: 150 }, { duration: "1m", target: 0 } ],
  thresholds: { http_req_failed: ["rate<0.001"], http_req_duration: ["p(95)<800"] },
};
const BASE = __ENV.BASE_URL || "http://localhost:8000";
const accts = ["ACC001", "ACC002", "ACC003", "ACC004"];
export default function () {
  const a = accts[Math.floor(Math.random() * 4)];
  let b = accts[Math.floor(Math.random() * 4)]; if (b === a) b = accts[(accts.indexOf(a) + 1) % 4];
  const r = http.post(`${BASE}/transfers`, JSON.stringify({ from_account: a, to_account: b, amount_kobo: 1000 + Math.floor(Math.random() * 500000) }),
    { headers: { "Content-Type": "application/json" } });
  check(r, { "accepted": (res) => res.status === 202 });
  sleep(1);
}
