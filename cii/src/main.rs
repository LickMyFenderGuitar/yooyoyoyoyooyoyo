use termion::{async_stdin, input::TermRead, raw::IntoRawMode};
use std::io::{self, Write};
use std::process::{Command, Stdio};

fn main() -> io::Result<()> {
    let stdout = io::stdout();
    let mut stdout = stdout.lock().into_raw_mode()?;

    // Set the terminal to raw mode
    write!(stdout, "{}", termion::clear::All)?;
    stdout.flush()?;

    // Start the shell
    run_shell()?;

    Ok(())
}

fn run_shell() -> io::Result<()> {
    let mut child = Command::new("bash")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()?;

    // Handle input and output
    let mut stdout = io::stdout().into_raw_mode()?;
    let stdin = async_stdin();

    write!(stdout, "Type 'exit' to quit the terminal emulator.")?;
    stdout.flush()?;

    // Read user input from the terminal and send it to the bash process
    for c in stdin.keys() {
        match c? {
            termion::event::Key::Char('q') => {
                write!(stdout, "Exiting...\n")?;
                stdout.flush()?;
                break; // Exit on 'q'
            }
            termion::event::Key::Char(c) => {
                // Send typed character to bash input
                if let Some(stdin) = &mut child.stdin {
                    write!(stdin, "{}", c)?;
                }

                // Print it on the screen
                write!(stdout, "You pressed: {}", c)?;
                stdout.flush()?;
            }
            termion::event::Key::Char('\n') => {
                // Send Enter to bash and execute the command
                if let Some(stdin) = &mut child.stdin {
                    write!(stdin, "\n")?;
                }
                
                // Read output from bash and print it
                if let Some(mut stdout_child) = child.stdout.take() {
                    let mut buffer = Vec::new();
                    stdout_child.read_to_end(&mut buffer)?;
                    write!(stdout, "Output: {}", String::from_utf8_lossy(&buffer))?;
                }

                stdout.flush()?;
            }
            _ => {}
        }
    }

    Ok(())
}
