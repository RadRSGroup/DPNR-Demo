# Core Persona Onboarding Funnel Demo

A simple HTML demo that simulates the onboarding funnel for the Core Persona platform, capturing user interactions and effectiveness metrics.

## Features

- Multi-phase flow (Registration → Quick-Fire → Primary Assessment → Confirmation)
- Progress tracking and metrics collection
- Responsive design for desktop and mobile
- Recursive feedback mechanism
- Metrics dashboard

## Setup

1. Clone or download this repository
2. Open `index.html` in a web browser
3. No additional setup required - it's a static HTML/CSS/JS application

## Usage

1. **Registration Phase**
   - Enter your email (required)
   - Enter your first name (optional)
   - Agree to the privacy policy
   - Click "Begin Assessment"

2. **Quick-Fire Phase**
   - Answer two quick-fire questions
   - Click "Continue to Primary Assessment"

3. **Primary Assessment Phase**
   - Answer two scenario-based questions
   - Click "Complete Assessment"

4. **Confirmation Phase**
   - View your persona type and confidence score
   - If confidence is low, you'll have the option to provide feedback

5. **Metrics Dashboard**
   - View detailed metrics about your assessment
   - See time spent in each phase
   - View completion statistics

## Technical Details

- Built with vanilla JavaScript
- Uses Bootstrap 5 for responsive design
- No backend required - all data is stored in browser memory
- Metrics are tracked in real-time

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Development

To modify or extend the demo:

1. Edit `index.html` for structure changes
2. Modify `styles.css` for styling updates
3. Update `app.js` for logic and functionality changes
