# Jupyter-Notebook-Tools
Python data tools created in Jupyter notebooks: examples and fully functional tools.

NOTE: Once the drift tool v1.0.0 is released, a video user guide will be shared for that tool. This README is more general and less specific and the information inside it should be usable across the tools.

This folder contains a growing number of Python data tools. To use these tools you will need access to the correct data sets, just as you'd need the Annex A to run the ChAT excel tool. Some of these tools are representations of tools that D2I currently makes for excel, such as the ChAT tool and disproportionality tool (though the have either all or most of the same functionality), and are designed to give you a flavour of the kind of thing that Python can do by comparing the Python tools to the excel tools. Other tools are independent and fully fledged tools in their own right, such as the DRIFT tool. This tools folder contains both completed versions of the tools, and completed versions of the tools which have had some or most lines of code deleted, but with extra comments added to the code. These notebooks with code deleted are meant to be used as exercises to help users work through writing these tools themselves, with prompts, to learn Python, knowing that completed examples exist if users get stuck.

The notebook tools presented here are intended to be able to be used with little to know Pytjon knowledge if all users want is the outputs. A general guide to setting up and using these tools is found in the following paragraphs. These tools are written in Jupyter notebooks with large markdown sections before each piece of code to help newer Pythonistas understand them and read them. They are also commented far more than production Python code would be, this is for the same reason. Whilst Python code can be read as plain english by experienced users, that's not always the best way to do things for early users, or people who just want to get the outputs without spending much time learning Python. A huge benefit of these tools being written in Python, particularly notebooks, is how easy it is to see what calculations and data work is being done to get from input to output data, unlike excel where this is often hidden in cells. Also, this method of sharing the code means that, once the code is up and running as it should be, it's really easy to make any changes to the inputs, outputs, or calculations. This means that users can easily change how data is analysed, what outputs are used and visualised, and how the visualisations look to match their LAs needs.

Each tool requires a little setup to run, but this is not really more setup than any of our excel tools take, so, whilst being confronted with the file may look intimidating, setup doesn't really require more than adding some filenames and column titles into the correct areas, which is indicated in the notebooks. Once you know these things, it's just a case of copy-pasting the info into the right places. Normally, to run each tool you will need just three things: 
  
  1) The filepath or directory where the excel or csv file your data is in is stored, this may look something like: 
      \\eschdata\Strategic_Resourcing_CS$\Performance Improvement Team\Data to Insight\Will\DRIFT Tool
  2) The filename, or file names, of the excel or csv files where the data is, for instance in the Annex A, this is the name of each workbook.
  3) The names of some columns from each data table, for instance the DRIFT tool requires you to find out the column names from the excel workbooks for the date of a referral, the date of CIN and CP plans, and the date CLA statuses start, in addition to this the DRIFT tool needs you to know the name of the columns from each table or workbook with unique child IDs in.
  
This may seem like a fair bit to do, but most of our excel tools need you to copy in file locations, make sure files have the correct names, and column names are standardized, either that, or copy and paste your data in by hand too. Each of these python data tools has a setup section which, if completed, should be enough to run the tool and get the outputs you want. There will be sections with green text telling you what to put in each place, and all you need to do is copy paste the information like filename or column name in. These will generally be of a similar form to the following lines of code: 
  
  filepath = r'####' (the r helps python read file paths, don't worry about it at this stage)
  filename = '####'
  user_column_1 = '####'
  
where you replace the hashes between the quote mark with you filepath, so you'd end up with something like:
  
  filepath = r'\\eschdata\Strategic_Resourcing_CS$\Performance Improvement Team\Data to Insight\Will\DRIFT Tool' 
  filename = 'Annex A List 1'
  user_column_1 = 'legacy_id' 
  
What this does is it creates variables called filepath, filename, etc. What this means is that every time you write the variable's name, like filepath, into your code, it tells Python that you actually mean r'####' or whatver your actual filepath is. It may help to explain this with algebra. We may write something like this into Python:

  x=1
  y=3
  z = x + y

As, once we have set the value of the variables, Python knows that x is 1 and y is 3, when we tell python that z is x + y, it knows that z is 4. This is the same with the variables we have initialised. If we write something like:

  os.chdir(filepath)

Which is a ine of code that tells Python to look in a particular filepath when looking for the files you are aksing it to look for, it knows that you really mean:

  os.chdir(r'\\eschdata\Strategic_Resourcing_CS$\Performance Improvement Team\Data to Insight\Will\DRIFT Tool')
  
The reason the setup portion of the code puts things like file paths, file names, and column names into variables is that, once you, as the user, have put it in once, the code can repeatedly use your input to function, rather than asking you to paste it in multiple times into the code. For instance, a couple of lines of code may be something like:
  new_table_1 = pd.read_csv(filename, sheet_name = user_column_1)
  new_table_2 = pd.read_ces(filename, sheet_name = user_column_2)
If the code did not setup variables like filename and user_column_1, every time these columns and filenames were needed, the user would have to find where they were used in the code needed and input them manually.

Once you have completed the setup portion of the notebooks by simply copy-pasting the right names into the right varaiables, getting the output of the code should be as simple as navigating to the buttons at the top of the notebook that look like the play, stop, and fast forward buttons from a casette player and pressing the fast forward button. What this fast forward looking button does is run every single box (cell) of code in the notebook. If you were to press just the play button (labeled run), it would only run the code from selected boxes, not the whole thing. If you did this and wanted the visualisations output at the end of the code, you would have to keep hitting the play/run button until every cell has finished running. The play/run button is useful, however, for instance if you want to run only a single cell.
IF, once you've run all of the code you scroll through it, the visualisations of the data can be found throughout the notebook, generally at the end, ready to either be copy-pasted into reports, or shared as dashboards.
