# story-orb-counter

Gets the total and individual spirit orb count from stories (main story, side story, TYBW story, sub story, event, chronicles). Data is parsed from https://bbs-simulator.com/story.

## Orb Count
If you just want to see the orb count instead of running it:\
Last Updated (MM/DD/YYYY): **9/2/2021**

Main Story Total Orb Count:  **3110** \
Side Story Total Orb Count:  **5248** \
TYBW Story Total Orb Count:  **586**\
Sub Story Total Orb Count:  **2612**\
Event Total Orb Count:  **25278**\
Chronicles' Total Orb Count:  	**467**

## Setup
1) Download or clone repository. 
2) Download [chromedriver](https://chromedriver.chromium.org/downloads).
3) Place it in the project directory or wherever you prefer. (By default it looks for chromedriver.exe in story-orb-counter/chromedriver/) 
	* If you place chromedriver.exe anywhere else, please modify `main.py` line 9 for your location.

## Usage
* Run main.py normally through command line.

* To output to a text file run as:
 
  ```python
  main.py > output.txt
  ```

## Dependencies
* BeautifulSoup4  4.9.3
* Selenium 3.141.0

## Credits
Big thank you to [Souldex](https://www.patreon.com/Souldex) for creating the [BBS Simulator](https://bbs-simulator.com/) website.
## License
[MIT](https://choosealicense.com/licenses/mit/)
