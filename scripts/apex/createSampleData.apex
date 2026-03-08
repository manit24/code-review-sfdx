// Sample data creation script for Growth Tracker App
// This script creates sample records to demonstrate the app functionality

public class CreateSampleData {
    
    public static void createSampleRecords() {
        // Create sample Accounts
        List<Account> accounts = new List<Account>();
        accounts.add(new Account(Name='Acme Corporation', Type='Customer'));
        accounts.add(new Account(Name='Globex Industries', Type='Customer'));
        accounts.add(new Account(Name='Initech Inc.', Type='Customer'));
        
        if (!accounts.isEmpty()) {
            insert accounts;
        }
        
        // Create sample Users (assuming these exist in your org)
        List<User> users = new List<User>();
        
        // Try to find existing users or create sample users
        // First, let's try to find some existing users
        List<User> existingUsers = [SELECT Id, Name, Email FROM User WHERE Name LIKE '%Test%' LIMIT 3];
        
        if (existingUsers.size() == 0) {
            // Create sample users if none exist
            users.add(new User(
                Alias = 'test1',
                Email = 'test1@example.com',
                EmailEncodingKey = 'UTF-8',
                LastName = 'Test',
                LanguageLocaleKey = 'en_US',
                LocaleSidKey = 'en_US',
                ProfileId = [SELECT Id FROM Profile WHERE Name = 'Standard User'].Id,
                Username = 'test1@example.com.test'
            ));
            
            users.add(new User(
                Alias = 'test2',
                Email = 'test2@example.com',
                EmailEncodingKey = 'UTF-8',
                LastName = 'Test2',
                LanguageLocaleKey = 'en_US',
                LocaleSidKey = 'en_US',
                ProfileId = [SELECT Id FROM Profile WHERE Name = 'Standard User'].Id,
                Username = 'test2@example.com.test'
            ));
            
            users.add(new User(
                Alias = 'admin',
                Email = 'admin@example.com',
                EmailEncodingKey = 'UTF-8',
                LastName = 'Admin',
                LanguageLocaleKey = 'en_US',
                LocaleSidKey = 'en_US',
                ProfileId = [SELECT Id FROM Profile WHERE Name = 'System Administrator'].Id,
                Username = 'admin@example.com.test'
            ));
            
            if (!users.isEmpty()) {
                insert users;
            }
        }
        
        // Get the users we'll use
        List<User> testUsers = [SELECT Id, Name FROM User WHERE Name LIKE '%Test%' OR Name = 'Admin' LIMIT 3];
        
        // Create sample Scorecards
        List<Scorecard__c> scorecards = new List<Scorecard__c>();
        
        for (Integer i = 0; i < 3; i++) {
            if (i < testUsers.size() && i < accounts.size()) {
                scorecards.add(new Scorecard__c(
                    Name = 'Scorecard for ' + testUsers[i].Name,
                    OwnerId = testUsers[i].Id,
                    Account__c = accounts[i].Id
                ));
            }
        }
        
        if (!scorecards.isEmpty()) {
            insert scorecards;
        }
        
        // Create sample Scorecard Entries
        List<Scorecard_Entry__c> entries = new List<Scorecard_Entry__c>();
        
        // Get the area definitions to know what areas to score
        List<Area_Definition__mdt> areas = [SELECT Id, Name FROM Area_Definition__mdt];
        
        // Get the score scales
        List<Score_Scale__mdt> scores = [SELECT Id, Name, Value__c FROM Score_Scale__mdt ORDER BY Value__c ASC];
        
        // Create sample entries for each scorecard
        for (Scorecard__c sc : scorecards) {
            for (Area_Definition__mdt area : areas) {
                // Pick a random score from the scale
                Integer randomIndex = Math.mod(System.currentTimeMillis(), scores.size());
                Score_Scale__mdt selectedScore = scores[randomIndex];
                
                entries.add(new Scorecard_Entry__c(
                    Name = 'Entry for ' + area.Name,
                    Scorecard__c = sc.Id,
                    Area__c = area.DeveloperName,
                    Score__c = selectedScore.Value__c,
                    Comments__c = 'Sample comment for ' + area.Name + ' area'
                ));
            }
        }
        
        if (!entries.isEmpty()) {
            insert entries;
        }
        
        System.debug('Created sample data for Growth Tracker App');
        System.debug('Accounts: ' + accounts.size());
        System.debug('Users: ' + testUsers.size());
        System.debug('Scorecards: ' + scorecards.size());
        System.debug('Entries: ' + entries.size());
    }
}
