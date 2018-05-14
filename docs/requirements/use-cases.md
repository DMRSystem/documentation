# Use Cases
### U1: Add Song via Command Line (with Command Line Arguments)

**Description:**

Radio Host adds a song to the system using the CLI and command line arguments.

**Actor(s):** Radio Host

**Preconditions:** Song is not in System

**Postconditions:** Song is in System

**Steps:**

1) Radio host enters the command:
```bash
dmr add song <songFile> --name=<songName> --artist=<songArtist> --year=<songYear>
```
2) System records the song locally and in remote repository.

**Alternate:**

2) System cannot connect to remote repository.

3) System displays `Cannot connect to remote repository.`

---

2) System cannot find file specified.

3) System displays `Cannot find the specified audio file.`

**Features: **[F1](features/#f1-add-song-via-command-line)


### U2: Add Song via Command Line (without Command Line Arguments)

**Description:**

Radio Host adds a song to the system using the CLI, but without command line arguments.

**Actor(s):** Radio Host

**Preconditions:** Song is not in System

**Postconditions:** Song is in System

**Steps:**

1) Radio host enters the command:
```bash
dmr add song
```
2) System prompts user for the song file.

3) User inputs the song filename/filepath.

4) System prompts user for the song title.

5) User inputs the song title.

6) System prompts the user for the song artist.

7) User inputs the song artist.

8) System prompts user for the song year.

9) User inputs the song year.

10) System records the song locally and in the remote repository.

**Alternate:**

3) User inputs empty filename.

4) System displays "Cannot add file with no file name."

5) System exits gracefully.

---

3) User inputs nonexistent file.

4) System displays "Cannot find specified file."

5) System exits gracefully.

At any other point, if the user enters an empty value, the system enters the default value (empty string).

**Features: **[F1](features/#f1-add-song-via-command-line)

