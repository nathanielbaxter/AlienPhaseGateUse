# -- This script generates the AlienPhaseGateUse mod.
# Use this python script to regenerate (and then update) the mod
# everytime the "ns2/lua/Alien.lua" file is updated by a new build.

import sys
import os
import re

# Modification constants for the Alien.lua file.
filename = "Alien.lua"
scriptline = 'Script.Load("lua/PhaseGateUserMixin.lua")\n'
addvarsline = "AddMixinNetworkVars(PhaseGateUserMixin, networkVars)\n"
initline = "    InitMixin(self, PhaseGateUserMixin)\n"

# Modification constants for the PhaseGateUserMixin.lua file.
filename2 = "PhaseGateUserMixin.lua"
regex = re.compile("GetEntitiesForTeamWithinRange\(\"PhaseGate\",\s+" +
    "([^\s,]+),\s+([^\s,]+),\s+([^\s,]+)\)")
replace = "GetEntitiesWithinRange(\"PhaseGate\", \\2, \\3)"

# Check for correct arguments.
if len(sys.argv) != 2:
	print ("""Generates the Alien.lua and PhaseGateUserMixin.lua files.
Usage: python GenerateMod.py luadir
  -- luadir: Location of the folder containing the clean Alien.lua file.""")
	exit()

# Check that the clean file exists.
if not os.path.exists(sys.argv[1] + "/" + filename) \
    or not os.path.exists(sys.argv[1] + "/" + filename2):
  print ("One or more required files were not found in the given luadir.")
  exit()

# Create the mod lua directory if needed.
if not os.path.exists("mod/lua"):
  os.mkdir("mod/lua")

# Delete any old Alien.lua file.
if os.path.exists("mod/lua/" + filename):
  os.remove("mod/lua/" + filename)

# Delete any old 
if os.path.exists("mod/lua" + filename2):
  os.remove("mod/lua/" + filename2)

# Open the files to read/write
fread = open(sys.argv[1] + "/" + filename, 'r')
fwrite = open("mod/lua/" + filename, 'w')

# Various stages
scriptload = False
addvars = False
init = False

for line in fread.readlines():
  fwrite.write(line)

  if not scriptload and line[:12] == "Script.Load(":
    fwrite.write(scriptline)
    scriptload = True
  elif not addvars and line[:20] == "AddMixinNetworkVars(":
    fwrite.write(addvarsline)
    addvars = True
  elif not init and line[:19] == "    InitMixin(self,":
    fwrite.write(initline)
    init = True

fread.close()
fwrite.close()

# Open the files to read/write
fread = open(sys.argv[1] + "/" + filename2, 'r')
fwrite = open("mod/lua/" + filename2, 'w')

num_replacements = 0
for line in fread.readlines():
  nline = re.sub(regex, replace, line)
  if not nline == line:
    num_replacements = num_replacements + 1
  fwrite.write(nline)

fread.close()
fwrite.close()

if not scriptload:
  print ("Failed to add Script.Load call")

if not addvars:
  print ("Failed to add AddMixinNetworkVars call")

if not init:
  print ("Failed to add InitMixin call")

if num_replacements == 0:
  print ("Failed to perform mixin code changes")
