# SwingSage
A comprehensive golf analysis tool for tracking rounds and handicaps as well as looking at all sorts of metrics. I am frustrated by the paywall for all kinds of golf stats/handicap tracking so the plan is to try to make this as open as possible, assuming I can pay for it. I want weekend golfers to be able to analyze their game with the same stats that pro golfers have without weekend golfers needing to buy super expensive equipment or pay for a costly subscription.

This app is currently in very early development and will likely take a while before it's in a usable form. The current plan for SwingSage is outlined below.

### Version 1
There will be a club selector and a next shot button that submits the data to the API. This location will be compared to each location to get distances and allow the user to keep track of their shot distances. This will be very rudimentary at first. This will also be accompanied by rudimentary buttons and things to get stats, handicap, etc. I plan on putting most of the stats in v1 of the app. The plan in this version is for this to be a simple website and might only be hosted locally with strict access control.

### Version 2
Version 2 will hopefully ramp up the complexity a bit by using the Google Maps API to get more detailed data on shots. I'm hoping that this version will also include some sort of computer vision to detect whether or not the user is on the fairway, green, tee box, or in the rough. I think I also have a strategy for this app to automatically pull which tee the user plays from on each hole so that users can play mixed tee rounds and have accurate stats. This version will also hopefully automatically query the USGA for a course's slope and rating.

### Unknown timeline
- [ ] Add scorecard detector that will pull all relevant data from a scorecard using object detection and OCR
- [ ] Open this up to approved users and friends/family for testing

### Maybe will never happen but would be pretty sweet
- [ ] Make Android/iOS apps for general use (probably gonna have ads)
- [ ] Apple/Galaxy/Pixel watch support for detailed swing tracking and automatic shot tracking

## Development Setup

```bash
pip install "swingsage @ git+ssh://git@github.com/rmsmith251/SwingSage.git"

# Install all dev dependencies (tests etc.)
pip install -e "swingsage[dev] @ git+ssh://git@github.com/rmsmith251/SwingSage.git"

# Setup pre-commit hooks
pre-commit install
```

## Frontend
I am using next.js for the frontend to make a React app. I'm pretty new to frontend stuff so my instructions here could be wrong but you'll definitely need [node.js](https://nodejs.org/en) installed. Once that's installed, you can run the dev server using
```bash
cd sage-frontend
npm run dev
```