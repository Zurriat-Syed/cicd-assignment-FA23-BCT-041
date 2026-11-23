# cicd-assignment-FA23-BCT-041

Lab Assignment 3 (Cloud Computing, FA 2026) - Syed Zurriat Hussain, FA23-BCT-041

- `index.html` - the web page (name, roll number, button, text box + Submit)
- `Dockerfile` - serves the page with nginx
- `tests/Dockerfile` - test agent (Python, Selenium, pytest, Chromium, ChromeDriver)
- `tests/test_site.py` - Selenium tests
- `Jenkinsfile` - Checkout, Package, Start Staging, Test, Deploy

## Run the tests manually

```bash
docker build -t cicd-site .
docker network create staging-net
docker run -d --name staging --network staging-net --network-alias staging cicd-site
docker build -t cicd-site-tests tests
docker run --rm --network staging-net -e BASE_URL=http://staging -v "$PWD/results:/results" cicd-site-tests
```
