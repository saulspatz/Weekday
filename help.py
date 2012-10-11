OddPlus11Text = '''\nThis program provides training in John Horton Conway's "Doomsday algorithm for mentally calcluating the day of the week.
A discussion of the algorithm can be found at http://en.wikipedia.org/wiki/Doomsday_algorithm.\n
The algorithm uses the "Odd + 11" improvement of Fong and Walters, discused at http://arxiv.org/ftp/arxiv/papers/1010/1010.0765.pdf\n
The program uses the "astronomical year," which assumes that the Gregorian calendar has been in use indefinitely far into the past, and will be used indefinitely far into the future.  It also assumes that there was a year zero.\n
If you give the incorrect answer, the program will display calculations leading to the correct answer, according to a variant of Conway's algorithm.\n
1. Reduce the year, whether A.D. or B.C. modulo 400, until you arrive at a number less than 400. For example, reduce 1979 to 379. No matter how big the year is, only the last 4 digits matter.\n
2. If the year is B.C. subtract it from 400.\n
3. For every hundred years since the year 0, count 5.  (Mnemonic: count centuries on your fingers.)  Call this the doomscentury.  For example, for the year 379, we would count 3 times 5, or 15.  (Since we'll be working modulo 7, you can reduce 15 to 1 at this point, if you like.)  From now on, we work with only the last two digits of the year, so we would change 379 to 79.\n
4. If the year (last two digits) is odd, add 11.  For example 79 is odd so 79 + 11 = 90\n
5. Divide the year by 2.  90/ 2 = 45\n
6. If the result is odd, add 11:  45 + 11 = 56\n
7. Reduce the result mod 7: 56 (mod 7) = 0\n
8. Subtract the result from 7: This gives 7, but we're working mod 7, so just leave it as 0.\n
9. Add the result to the the doomscentury, then reduce the sum modulo 7.  In our example, we have 15 + 0 = 15 and 15 (mod 7) = 1.  Call this the doomsyear.\n
10. The doomsday for the year zero was Tuesday.  (Mnemonic: "Doomsday" and "Tuesday" are assonant.)  Add the doomsyear to Tuesday to get the doomsday for the year in question.  In our example, the doomsday for 379 is 1 day after Tuesday, or Wednesday.\n
11. Once you know the doomsday, compute the weekday by Conway's method.
\nhere are many different ways to calculate the doomsday.  This method is the one the author has found quickest to calculate.
\nIt should be straightforward to modify the program to use additional algorithms.
\nIf you don't want to use the astronomical year, the program will need more extensive changes.'''

LeapYearsText = '''\nThis program provides training in John Horton Conway's "Doomsday algorithm for mentally calcluating the day of the week.
A discussion of the algorithm can be found at http://en.wikipedia.org/wiki/Doomsday_algorithm.\n
The program uses the "astronomical year," which assumes that the Gregorian calendar has been in use indefinitely far into the past, and will be used indefinitely far into the future.  It also assumes that there was a year zero.\n
If you give the incorrect answer, the program will display calculations leading to the correct answer, according to a variant of Conway's algorithm.\n
1. Reduce the year, whether A.D. or B.C. modulo 400, until you arrive at a number less than 400.  No matter how big the year is, only the last 4 digits matter.\n
2. If the year is B.C. subtract it from 400.\n
3. For every hundred years since the year 0, count 5.  (Mnemonic: count centuries on your fingers.)  For example, for the year 379, we would count 3 times 5, or 15.  From now on, we work with only the last two digits of the year, so we would change 379 to 79.\n
4. Divide the year by 4 to get the number of leap years that have passed.  Ignore any remainder.  For 79, this would give us 19.\n
5. Add the year, the number of leap years, and the century value, then reduce the result modulo 7.  In our example, we have 79 + 19 + 15 = 113 and 113 (mod 7) = 1.  Call this the delta value.\n
6. The doomsday for the year zero was Tuesday.  (Mnemonic: "Doomsday" and "Tuesday" are assonant.)  Add the delta value from the previous step to Tuesday to get the doomsday for the year in question.  In our example, the doomsday for 378 is 1 day after Tuesday, or Wednesday.\n
7. Once you know the doomsday, compute the weekday by Conway's method.
\nThere are many different ways to calculate the doomsday.  This method is the one the author has found easiest to remember.
\\nIt should be straightforward to modify the program to use additional algorithms.
\nIf you don't want to use the astronomical year, the program will need more extensive changes.'''

mnemonicText =  '''\nMnemonics for doomdays:\n
For even months (except February) the day's the same as the month:\n
    4/4, 6/6, 8/8, 10/10, 12/12\n
Odd months (after March) get swapped:
    5/9, 9/5, 7/11, 11/7  "Work 9 to 5 at the 7-11."\n
March is easy: The last day of February is a doomsday, so use 0.
    "Nothing to remember."\n
For February, we can use 1 in a leap year, 0 in a non-leap year.
    "February is the leap month."\n
For January, we can use 4 in a leap year, 3 in a non-leap year.
    "Three out of four years are non-leap years."\n
In leap years, we have new mnemonics for January and February:
    1/11 and 2/22
For non-leap years we have 1/10 and 2/21
    "A non-leap year has one day less than a leap year."\n'''


