# ADS FS 2024

## Local dev
For linux hosts only. Allow x11 windows to be forwarded.
```
sudo xhost +
```

## Cloud Run

Initial cloud run setup setup.
```
gcloud beta run jobs replace scraper/infra/job.yaml
gcloud beta run jobs replace transform/infra/job.yaml
```