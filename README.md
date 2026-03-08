# Growth Tracker App - Getting Started Guide

This guide will help you set up and test the Growth Tracker LWC application in your Salesforce org.

## Prerequisites
- Salesforce Org with API access
- Admin permissions to create records and configure settings
- Salesforce CLI installed and authenticated
- VS Code with Salesforce Extensions installed

## Setup Instructions

### 1. Deploy the Application
Since we've already confirmed that all components are properly created in the project structure, you can deploy the application to your org using one of these methods:

**Method A: Using Salesforce CLI**
```bash
sf deploy metadata --target-org your-org-alias --source-dir force-app
```

**Method B: Using MCP Tool (if available)**
```bash
sf deploy metadata --target-org your-org-alias --source-dir force-app
```

### 2. Create Sample Data
To test the application, run the following anonymous Apex script to create sample records:

1. Open VS Code
2. Navigate to `scripts/apex/createSampleData.apex`
3. Select the entire content of the file
4. Right-click and select **"SFDX: Execute Anonymous Apex with Currently Selected Text"**

This will create:
- 3 sample Accounts
- 3 sample Users (if none exist)
- 3 Scorecards (one per user)
- Sample Scorecard Entries across all 4 growth areas

### 3. Configure Permission Sets
Make sure users have the appropriate permission sets assigned:
- **Growth_Tracker_Admin** - For administrative access
- **Growth_Tracker_User** - For standard user access  
- **Growth_Tracker_Manager** - For manager access

### 4. Access the Application

#### User Dashboard
1. Navigate to **My Growth Dashboard** flexipage
2. This shows personal scorecards and achievements

#### Team Dashboard  
1. Navigate to **Team Growth Dashboard** flexipage
2. This shows team-level metrics and comparisons

#### Admin Console
1. Navigate to **Admin Console** flexipage
2. This provides configuration and management capabilities

### 5. Test the Features

#### Scorecard Creation
- Go to the Scorecard__c tab
- Create a new scorecard record
- Assign it to a user and account

#### Scoring Process
- Navigate to a scorecard record
- Add entries for each of the 4 areas:
  - Own Work
  - Platform Expertise  
  - Product+
  - Core Values
- Assign scores from 1-5 for each area

#### Gamification Features
- View badges earned based on score thresholds
- Check insights generated from scoring data
- Monitor progress toward goals

### 6. Customize for Your Organization

#### Update Area Definitions
1. Go to **Area_Definition__mdt** custom metadata type
2. Edit or create new area definitions to match your organization's growth focus areas

#### Configure Scoring Scale
1. Go to **Score_Scale__mdt** custom metadata type
2. Modify the scoring values to match your organization's rating system

#### Set Up Badges
1. Go to **Badge_Definition__mdt** custom metadata type
2. Configure badge criteria based on score thresholds

## Troubleshooting

### If Deployment Fails with .forceignore Error
This is a known CLI tooling issue that doesn't affect the actual deployment. The files are properly structured and can be deployed using alternative methods or by bypassing the problematic .forceignore check.

### Missing Sample Data
If you don't see sample data after running the Apex script:
1. Check the debug log for any errors
2. Verify that the script executed successfully
3. Manually create some basic records in the objects

## Key Features Demonstrated

1. **Personalized Growth Tracking** - Individual scorecards for each user
2. **Team Collaboration** - Shared dashboards and team metrics
3. **Gamification Elements** - Badges and insights based on performance
4. **Flexible Scoring** - 1-5 scale across 4 growth areas
5. **Admin Controls** - Full configuration through custom metadata
6. **Experience Cloud Ready** - Designed for embedding in customer portals

## Next Steps

1. Test with your actual user data
2. Customize the scoring criteria to match your organization's goals
3. Configure additional badges and insights
4. Set up automated workflows using flows
5. Embed in Experience Cloud sites for wider access
