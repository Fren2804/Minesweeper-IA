# 🧨 Minesweeper in Python

> 🇬🇧 English | [🇪🇸 Versión en Español](README.es.md)

## 📌 Description

This project consists of creating a bot to automatically play the classic **Minesweeper** game. There are **two versions of the program**:

- A **complete and functional** version, located in the main directory, which uses the **PyAutoGUI** library.
- An **incomplete** version, located in a subdirectory, which was developed with the **Selenium** library.

## 🚀 Motivation and Evolution

I started developing the bot with Selenium. I managed to complete the first phase, which was identifying the mines and clicking on the safe cells. However, the performance was very slow, so I looked for faster alternatives. That’s when I discovered PyAutoGUI, which turned out to be much more efficient for this case.

---

## 🧪 Selenium Version

This version requires a **Chrome driver**. When running the program, a browser window opens with a message indicating that it is being automated. This can be an issue on websites that block automation, and it’s something to keep in mind for future projects.  

### ❌ Limitations

- Selenium loads all page elements (HTML, CSS, etc.), which makes it **very slow**.  
- Each time a click is made on a safe cell, the page **partially reloads**, making the process heavier.  
- In my tests:  
  - The **beginner** level was solved in about **7 seconds**.  
  - The **intermediate** level in approximately **18 seconds**.  
  - This is **far too slow** for an efficient bot.  

### ✅ Advantages

- By working directly with **DOM elements**, Selenium provides greater **flexibility** in terms of screen resolution, element positioning, and interaction accuracy.  
- The game elements are **easy to identify** thanks to their well-structured classes and identifiers.  

### 🧾 Minesweeper DOM Data

When inspecting the game’s HTML, it is easy to identify relevant information for each cell. For example:  

- The **class (`class`)** indicates the **state of the cell** (blank, revealed, number of nearby mines, etc.).  
- The **identifier (`id`)** provides the **position** of the cell in the format `row_column`.

#### Cell Examples:

- **Blank cell**, not revealed. It could contain a mine.  
  (x = 20, y = 8)  
  ```html
  <div class="square blank" id="8_20"></div>
  ```
- **Revealed cell with number 2**, indicating that there are two mines around it.
  (x = 16, y = 7)  
  ```html
  <div class="square open2" id="7_16"></div>
  ```

### 🎮 Game State

It is also possible to detect the game state (in progress, won, or lost) through a DOM element with the identifier `"face"` and a dynamically changing class:

- If the class is `"facesmile"`, it means the game is **still active**.
  ```<div class="facesmile" style="margin-left:182px; margin-right: 182px;" id="face"></div>```

### 📋 Summary of Useful Classes

| Class              | Meaning                                      |
|--------------------|----------------------------------------------|
| `square blank`       | Unrevealed cell (possible mine)              |
| `square open0`       | Revealed cell, 0 mines around                |
| `square open1`       | Revealed cell, 1 mine around                 |
| `square open2`       | Revealed cell, 2 mines around                |
| `square open3`       | Revealed cell, 3 mines around                |
| `square open4`       | Revealed cell, 4 mines around                |
| `square open5`       | Revealed cell, 5 mines around                |
| `square open6`       | Revealed cell, 6 mines around                |
| `square open7`       | Revealed cell, 7 mines around                |
| `square open8`       | Revealed cell, 8 mines around                |
| `square bombflagged` | Cell marked as possible mine                 |
| `facesmile`          | Game in progress                            |
| `facewin`            | You won                                     |
| `facedead`           | You lost                                    |

---

## 🧪 PyAutoGUI Version (Final)

This version does not need to interact with the browser or analyze the DOM. Instead, it **works directly on screenshots**, analyzing the **pixels** of the image or interacting with the pixels on your screen. The bot acts as if it were a real user.  

### ❌ Limitations

- Although PyAutoGUI allows searching for **visual patterns** or images on the screen, the **wider** the area you analyze, the **slower** the process will be.  
- If you use **exact pixel values**, the system is very fast but loses flexibility. If the page shifts even **one pixel**, the bot may stop working.  
- The higher the **precision** you require, the smaller the **margin of error** allowed.  
- It is necessary to perform a sort of **manual "data mining"** to identify which pixels or colors you want to capture and what they mean. In other words, you define your own dataset from the image.  

### ✅ Advantages

- Using exact **pixel coordinates and colors**, the bot is **extremely fast**.  
- Allows greater **optimization potential** than Selenium.  
- When clicking, there is **no need to reload the page** or wait for any transition.  
- In my tests:  
  - The **beginner** level was solved in about **1 second**.  
  - The **intermediate** level in around **3 seconds**.  
  - The **expert** level in about **10 seconds**.  
  - These times are **far superior** to those obtained with Selenium.  

### 📊 Example Data

Unlike Selenium, here the data is **defined by you** based on what you see on the screen. For example:  

```python
config.x_victory = 446 - config.screenshot_left
```  

This value (`x_victory`) represents the horizontal position (X coordinate) of the pixel where the victory face is displayed. It is calculated based on the offset of the captured area.

Another example:
```python
(255, 0, 0): 3
``` 

This indicates that the pure **red color** `(255, 0, 0)` represents the number **3** on the board. It is a straightforward way to identify which number appears in a cell, based on the color of a pixel. As you can see, this technique requires manually defining the relevant values, but it gives you **full control** over how to interpret the image. You can use the `show` function to view the screenshot or save it and use a simple tool like Paint to measure and obtain the distances of the most relevant pixels.  

### 🧾 Conclusion

Although **PyAutoGUI** is not error-tolerant and requires **manual testing** to identify pixels and extract useful data, it offers **much faster performance** than Selenium.  It is a very effective tool when **execution speed** and **full control** over the environment are the priority, at the cost of less tolerance to visual changes and more initial setup work.  

---

## 🧪 Pixel Detection and Data Extraction

In the `sources` folder, you can find the different icons that the page uses to represent each element of the board. This is very useful for analyzing pixels and deciding what information to look for.  

![Icons](Minesweeper/Icons.png)

Once collected, the next step is to **analyze the elements and break them down as much as possible**, with the goal of reducing checks and generalizing the process as much as possible.  

### 🟨 In the Beginning

I used to crop each image directly from the screenshot provided by the page to compare the complete patterns. It worked, but it was slow and inefficient. After some research, I discovered that I could optimize the search by analyzing only **key pixels** instead of full images — since a 24×24 image means 576 pixels to check each time.  

### ✂️ My Breakdown

The first separation I made was to distinguish between:

- The minefield (board)  
- The smiley face panel  

### 🔲 Cells

With **150% zoom**, each cell takes up **24×24 pixels**. I use a pixel from the **top-left corner** to know whether the cell is pressed or not. To differentiate them, I rely on the white and gray colors `(192, 192, 192)`.  

![Squares](Minesweeper/Squares.png)

#### 🔢 Selected Cell (Numbers)

For selected cells, I need to obtain the number that appears. By analyzing the patterns, I found a very favorable row where almost all numbers have characteristic pixels. From there, I selected the pixels of **2** and **7**, since they are the most restrictive.  

![Numbers](Minesweeper/Numbers.png)

From this point, I can map the numbers using an **RGB color table**:  

```python
colors = {
    (192, 192, 192): 0,
    (0, 0, 255): 1,
    (0, 128, 0): 2,
    (255, 0, 0): 3,
    (0, 0, 128): 4,
    (128, 0, 0): 5,
    (0, 128, 128): 6,
    (0, 0, 0): 7,
    (128, 128, 128): 8,
}
```

#### 🚩 Unselected Cell

For unselected cells, there are two possible cases:  
- Empty  
- With a flag  

The difference can be easily detected by choosing a pixel in the center where there is a noticeable color variation.  

![BombFlagged](Minesweeper/Flagged.png)  

### 🙂 Smile

The smiley face has 3 possible states:  

- Playing (happy face)  
- Defeat (dead face)  
- Victory (face with sunglasses)  

To distinguish them, I selected restrictive pixels. First, I check whether the game has been won, since in the other two cases the corresponding pixel area is identical. The next difference is found in the mouth of the dead face.  

![Smiles](Minesweeper/Smiles.png)  

### 🖼️ Other Images

There are more icons and face variations, but they are not relevant. For example, if mines are revealed, we already know the game is lost (dead face). Other intermediate expressions do not provide essential information, since the important part is distinguishing **loss** and **victory**. That’s why, in this analysis, the main goal is to identify the **critical pixels** of the faces that allow us to determine the actual game state.  

---

### ⚙️ Configuration

In the configuration, I define the parameters required for the bot to work properly:  
- Steps between cells, very useful for working with **relative positions** instead of absolute coordinates.  
- The position of all **critical pixels**, which allow identifying key board states.  
- The number of rows and columns depending on the selected difficulty (beginner, intermediate, or expert).  
- The **reference colors**, used to differentiate cells, numbers, and flags.  

---

### 💾 Data Storage

The board information is stored in an **internal representation table**, where each symbol indicates a state:  

- `X` → Mine.  
- `-` → Blank or unknown cell.  
- Number (0–8) → Number of mines around the cell.  
- `?` → Unknown, this symbol is used internally when a cell is clicked but its data has not yet been loaded.  

```
###########
#11001X100#
#X10011100#
#110000000#
#011100000#
#12X101110#
#--2101X10#
#--1001221#
#--11111X2#
#--11X112X#
###########
```

---

## 🧩 Logic

The process begins by clicking on the **center of the board** to start the game and reveal the first cells. From there, the bot **loads the board data** and begins analyzing it.  

### 🔹 Phase 1 — EZ (Basic)

The first phase is the **simplest**: looking for **obvious mines**. First, I flag the mines, then I click on the safe cells.  

- If a **2** appears and there are only two possible cells around it, those two are **definite mines** → they are marked with `X`.  
- If a **3** appears, and I already have 2 safe mines detected, leaving only one free option, then that last one is also marked as a mine.  
- If a **2** appears, and I already have **2 mines flagged** around it and **2 remaining spaces**, then those spaces are **safe**, and the bot automatically clicks on them.  

In this phase, I only apply **direct and obvious deductions**, ensuring there is no margin for error.  

```
####
#11#
#-1#
####
#####
#---#
#-21#
#121#
#01X#
#####
```

⚠️❗ **Note:**  
From this point onward, although my implementation works, I believe it could be done **much better**. The current approach is **not the most optimal** — it is simply the solution I found to make the bot work correctly.  

### 🔹 Phase 2 — Blocks

The second phase begins **only if no changes are made in Phase 1**. I call this phase **“blocks”**.  

👉 What does this mean?  
**Blocks** are considered to be cells that have a **direct relationship with each other**. In other words, any modification in one cell immediately affects another that we have access to.  

- A cell surrounded only by mines and `-` provides no useful information.  
- On the other hand, it is only relevant if there are **visible numbers** around it (within a distance of 1).  

In the following image, the blocks are shown in color. In this situation, it would be possible to continue solving in the lower block, but I stopped the execution to show the example:  

![Blocks](Minesweeper/Blocks.png)  

#### 📝 Important Information in This Phase

- Do not move **diagonally**. By using the order (right → down ↓ left ← up ↑), the diagonals can still be reached if necessary.  
- Do not go back on your steps: if the order is (right → down ↓ left ← up ↑) and I moved left, I don’t go back to the right.  
- Beware of **loops**: a block may close back onto itself.  
- If searching by **rows** doesn’t yield results, try searching by **columns**.  
- There may be **more than one possible path** within the same block.  

### 🔹 Phase 3 — 💀 Imperfect

In the **blocks** phase, we only obtain **one block per process**. Once we have one, we move on to analyzing **hypothetical situations**:  

- What happens if I place a flag in the first position?  
- What about the second one?  
- And the third one?  

From these tests, three possible outcomes are generated:  

- **Impossible flag** → Ideal situation, meaning that this cell **100% cannot be a mine**, therefore it is safe.  
- **Valid solution** → A possible solution, but it does **not guarantee correctness**, since in other alternative scenarios it may not hold true.  
- **Poor information** → A situation where we get some bombs and safe zones, but they don’t mean anything conclusive.  

In my current implementation, I **take valid solutions as correct**, even though they are not always so. Here we enter the territory of **randomness** and **algorithmic limitations**.  

#### 📝 Solution Options

- Look for another **block** that allows solving the situation from a different path.  
- Save all analyzed cells and calculate the **probabilities** of each one being a mine or safe, selecting only those with guaranteed safety.  
- Use **specific known Minesweeper patterns** (e.g., the classic 1-2-1 or 1-2-2-1 formations).  

In this phase, **nothing is 100% certain**, and the process becomes **pseudo-random**.  

### 🔹 Phase 4 — ☠️ Random Death

The worst phase. It happens when a block is completely **isolated by mines**, and there is no logical way to access it. In that case, the only option is to make a **random click** and hope for survival.  

---

## 🏁 End

There are certain details that I have not explained in depth, such as:  

- If the bot dies at any point, it automatically restarts.  
- How often the data is refreshed.  
- The relationship between the different board sizes.  
- Fine-tuning and small implementation details.  

The important thing is that I’ve conveyed the **general concept** and the approach used, which I hope is now clear.  

---

## 📊 Results Obtained

![Results](Minesweeper/Records.png)

## 🎥 Demo Video

[![Watch the video](https://img.youtube.com/vi/Y5WTmX_FgSI/0.jpg)](https://www.youtube.com/watch?v=Y5WTmX_FgSI)
