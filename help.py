algorithmText = '''\nThis program provides training in John Horton Conway's "Doomsday algorithm for mentally calcluating the day of the week.'''
algorithmText += '''  A discussion of the algorithm can be found at http://en.wikipedia.org/wiki/Doomsday_algorithm.\n\n'''
algorithmText += '''The program uses the "astronomical year," which assumes that the Gregorian calendar has been in use indefinitely far into the past, and will be used indefinitely far into the future.  It also assumes that there was a year zero.\n\n'''
algorithmText += '''If you give the incorrect answer, the program will display calculations leading to the correct answer, according to a variant of Conway's algorithm.\n\n'''
algorithmText += '''1. Reduce the year, whether A.D. or B.C. modulo 400, until you arrive at a number less than 400.  No matter how big the year is, only the last 4 digits matter.\n\n'''
algorithmText += '''2. If the year is B.C. subtract it from 400.\n\n'''
algorithmText += '''3. For every hundred years since the year 0, count 5.  (Mnemonic: count centuries on your fingers.)  For example, for the year 379, we would count 3 times 5, or 15.  From now on, we work with only the last two digits of the year, so we would change 379 to 79.\n\n'''
algorithmText += '''4. Divide the year by 4 to get the number of leap years that have passed.  Ignore any remainder.  For 79, this would give us 19.\n\n'''
algorithmText += '''5. Add the year, the number of leap years, and the century value, then reduce the result modulo 7.  In our example, we have 79 + 19 + 15 = 113 and 113 (mod 7) = 1.  Call this the delta value.\n\n'''
algorithmText += '''6. The doomsday for the year zero was Tuesday.  (Mnemonic: "Doomsday" and "Tuesday" are assonant.)  Add the delta value from the previous step to Tuesday to get the doomsday for the year in question.  In our example, the doomsday for 378 is 1 day after Tuesday, or Wednesday.\n\n'''
algorithmText += '''7. Once you know the doomsday, compute the weekday by Conway's method.'''
algorithmText += '''\n\nThere are many different ways to calculate the doomsday.  This method is the one the author has found easiest to remember and quickest to calculate.'''
algorithmText += '''\n\nIf you want to use a different method, you just have to modify Board.explain.'''
algorithmText += '''\nIf you don't want to use the astronomical year, the program will need more extensive changes.'''



