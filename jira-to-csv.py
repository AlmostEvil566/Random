from __future__ import print_function
import unicodecsv as csv
import atexit
import sys
import json
from jira import JIRA
from os import path
from json import dumps, loads
import io


sys.setrecursionlimit(100000)

jira = JIRA('https://r3-cev.atlassian.net', auth=('max.powers@r3.com', 'Boscopowers12'))
key_list = []
results = []


def jira_results(jira):
	jira_issues = jira.search_issues('project in (ENT, CID, CORDA) AND status in ("Closed Duplicate", "Define", Defined, Designed, Done, "In Design", "In Progress", "New Idea", Open, "Pending Review", "Selected for Development", "Wont Do")', maxResults = 100)
	remainder = int(jira_issues.total)
	counter_pages = 0
	while remainder > 0:
		jira_issues = jira.search_issues('project in (ENT, CID, CORDA) AND status in ("Closed Duplicate", "Define", Defined, Designed, Done, "In Design", "In Progress", "New Idea", Open, "Pending Review", "Selected for Development", "Wont Do")', maxResults = 100, startAt=counter_pages)
		counter_items = 0

		for jira_issues[counter_items] in jira_issues:

			key = jira_issues[counter_items].key

			id_ = jira_issues[counter_items].id

			try:
				epic_name = jira_issues[counter_items].fields.customfield_10017
			except AttributeError:
				epic_name = "No Epic Name"	

			summary = jira_issues[counter_items].fields.summary

			try:
				assignee_ = jira_issues[counter_items].fields.assignee.displayName
			except AttributeError:
				assignee_ = "Unassigned"	

			status = jira_issues[counter_items].fields.status.name

			created = jira_issues[counter_items].fields.created

			try:
				epic_status = jira_issues[counter_items].fields.customfield_10016.value
			except AttributeError:
				epic_status = "No Epic Status"	
			try:
				epic_link = jira_issues[counter_items].fields.customfield_10015
			except AttributeError:
				epic_link = "No Epic Link"
			try:
				type_ = jira_issues[counter_items].fields.issuetype.name
			except AttributeError:
				type_ = "No Issue Type"
			try:
				storypoints = jira_issues[counter_items].fields.customfield_10021
			except AttributeError:
				storypoints = "No Storypoints"
			try:
				labels = jira_issues[counter_items].fields.labels[0]
			except Exception:
				labels = "No Label"
			try:
				sprint1 = jira_issues[counter_items].fields.customfield_10019[0]
				
				sprint2 = sprint1.split(',')
				sprint3 = sprint2[3].split('=')
				sprint = sprint3[1]
			
			except Exception:
				sprint = "No Sprint"
			try:
				resolution = jira_issues[counter_items].fields.resolutiondate
			except AttributeError:
				resolution = "Unresolved"
			team = jira_issues[counter_items].fields.resolutiondate
			full_issue = [key, id_, epic_name, summary, assignee_, status, created, epic_status, epic_link, type_, storypoints, labels, sprint, resolution, team]
			map(unicode,full_issue)
			results.append(full_issue)
			counter_items += 1
		counter_pages += 100
		remainder -= 100

	return results

header = ["Key", "ID","Epic_Name","Summary","Assignee","Status","Created","Epic Status", "Epic Link", "Type", "Storypoints", "Labels", "Sprint", "Resolution Date", "Team"]
all_results = [header] + jira_results(jira)
def read_counter():
    return loads(open("counter.json", "r").read()) + 1 if path.exists("counter.json") else 0


def write_counter():
    with open("counter.json", "w") as f:
        f.write(dumps(counter))


counter = read_counter()
atexit.register(write_counter)


with open('nameOfOutputFile{}.csv'.format(counter), 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',',quoting=csv.QUOTE_ALL, encoding="utf-8")
    for val in all_results:
        writer.writerow(val)
		
