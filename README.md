# Magoosh crash course to ICS

Script to convert Magoosh crash course into Calendar events


## Usage
```shell
git clone https://github.com/cyriac/magoosh-gre-crash-course-ics
cd magoosh-gre-crash-course-ics
pip install -r requirements.txt
python magoosh.py run --start dd/mm/yyyy --out event.ics
```

### Options

| Option        | Optional      | Default        | Description      |
| ------------- | ------------- | -------------- | ---------------- |
| `--start`     | :white_check_mark:  | Tomorrow in dd/mm/yyyy format   | Provide the date in dd/mm/yyyy format on when you want to start the course    |
| `--out`       | :white_check_mark:  | event.ics   | Provide the filename eg: `event.ics` to which the calendar event will be written     |
