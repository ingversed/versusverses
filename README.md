## versusverses 

versusverses generates mashed-up poetry from the works of two or more poets, using markov chains.

> In twenty years I was fresh and cheerful, who but I?

> Rushes in a net deliberately cast over the terrible pain,  
> I loved you for life, but life has quite gone by.

> – Christina Rossetti versus Sylvia Plath versus Louise Glück

First, create a 'PoemHunterTop500' folder in the same directory as the script. 

Then, run the poet scraper with no arguments. The program will prompt for the minimum number of poems required for a poet's corpus to be scraped. This will generate a json file of PoemHunter's Top 500 poets who have equal to or greater than the minimum number of poems. 

Then, run the corpus scraper with no arguments. This will generate a corpora text file for every poet in the json file.

Then, run the poem generator with no arguments -- it'll prompt you for a random and/or input selection of poets. The program will feed the selected corpora into the markovify combine harvester, with each corpus’ contribution to the mix weighted according to relative filesize. Currently, the program is configured for a 1-line/2-lines/2-lines/1-line stanza scheme, with the first and last lines acting as a refrain.

NOTE: Error handling is minimal and data cleansing is none (by design, as this occasionally results in some incredible lines).

> Death had the Mercy, you’re done with the smut and smog and smoke of our nights:

> They charmed it with care;  
> You and I see the shadows falling,

> It got up that afternoon–walked to the vibration thru the grocerystore,  
> Thou art slave to fate, chance, kings, and none but fair,

> Death had the Mercy, you’re done with the smut and smog and smoke of our nights.

> – Allen Ginsberg versus Lewis Carroll versus John Donne versus Anna Akhmatova

