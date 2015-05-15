__author__ = 'sdouglas'


import sqlite3
from XCCDF_Parser import Parse as xccdf_parser


# Connect to target database
conn = sqlite3.connect('linux_stig.db')

# Cursor is used to execute sql commands
c = conn.cursor()

# Create our STIG table.
# id ==> STIG Vuln ID (e.g. V-33432)
# check_command ==> The command run to check the status of the current stig
# fix_command ==> command or procedure to resolve the status of the current stig
# resolution ==> the status of the current stig (e.g. NR, O, NF, NA)
c.execute('''CREATE TABLE stigs
              (id text, check_command_debian text, check_command_redhat text, fix_command_debian text,
              fix_command_redhat text, resolution text)''')

# Parse our sample stig
xccdf = xccdf_parser("sample_files/redhat-stig/U_RedHat_6_V1R7_STIG_SCAP_1-1_Benchmark-xccdf.xml")
stig_list = xccdf.construct_dictionary()
# Loop through our resulting stig list so we can obtain every STIG ID
for item in stig_list:
    # When inserting a variable into a sqlite3 statement, use a tuple to prevent a little bobby tables incident
    t = (item['STIG_ID'],)
    # In case you couldn't guess, the ? is equivalent to %s
    c.execute("INSERT INTO stigs VALUES (?, '', '', '', '', 'NR')", t)

# Saves our modifications to the database
conn.commit()
# Close the database connection
conn.close()

print "Great Success!?"
