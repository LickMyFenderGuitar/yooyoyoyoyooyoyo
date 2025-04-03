use std::{io::{self, Write}};
use chrono::Local;
use tokio::time::{sleep, Duration};
use std::sync::{Arc, Mutex};

const RESET: &str = "\x1b[0m";
const BOLD: &str = "\x1b[1m";
const CYAN: &str = "\x1b[96m";
const YELLOW: &str = "\x1b[93m";
const GREEN: &str = "\x1b[92m"; // Used in About Flux section
const BLUE: &str = "\x1b[94m";  // Used in About Flux section
const CLEAR_SCREEN: &str = "\x1b[H\x1b[J";

fn display_terminal(current_time: &str, current_date: &str) {
    print!("{}", CLEAR_SCREEN);
    
    // UI Header
    println!("{}{}╔════════════════════════════════════════════╗{}", CYAN, BOLD, RESET);
    println!("{}{}║      flux terminal DEMO - Rust            ║{}", CYAN, BOLD, RESET);
    println!("{}{}╠════════════════════════════════════════════╣{}", CYAN, BOLD, RESET);
    println!("{}║  Time: {}{}   {}|  Date: {}{}  {}║{}", YELLOW, CYAN, current_time, YELLOW, CYAN, current_date, YELLOW, RESET);
    println!("{}{}╚════════════════════════════════════════════╝{}", CYAN, BOLD, RESET);
    
    // About Flux
    println!("\n{}{}╔════════════════════════════════════════════╗{}", CYAN, BOLD, RESET);
    println!("{}║  About Flux:                               ║{}", CYAN, RESET);
    println!("{}║  Flux is a programming language designed    ║{}", GREEN, RESET);
    println!("{}║  to be fast, lightweight, and easy to       ║{}", GREEN, RESET);
    println!("{}║  integrate into applications. It is built   ║{}", BLUE, RESET);
    println!("{}║  for low-level performance with simple      ║{}", BLUE, RESET);
    println!("{}║  integration into other systems.            ║{}", GREEN, RESET);
    println!("{}╚════════════════════════════════════════════╝{}", CYAN, BOLD, RESET);
}

#[tokio::main]
async fn main() {
    // Initialize time and date with placeholder values
    let current_time = Arc::new(Mutex::new("00:00:00".to_string()));
    let current_date = Arc::new(Mutex::new("0000-00-00".to_string()));
    
    // Start the time updating task asynchronously
    let time_thread_time = current_time.clone();
    let time_thread_date = current_date.clone();
    tokio::spawn(async move {
        loop {
            // Update the time and date every second
            let new_time = Local::now().format("%H:%M:%S").to_string();
            let new_date = Local::now().format("%Y-%m-%d").to_string();
            
            // Lock and update shared time and date
            {
                let mut time_lock = time_thread_time.lock().unwrap();
                let mut date_lock = time_thread_date.lock().unwrap();
                *time_lock = new_time;
                *date_lock = new_date;
            }
            
            sleep(Duration::from_secs(1)).await; // Sleep for 1 second
        }
    });

    loop {
        // Get current time and date (locked for thread safety)
        let current_time = current_time.lock().unwrap().clone();
        let current_date = current_date.lock().unwrap().clone();
        
        // Display the terminal with updated time and date
        display_terminal(&current_time, &current_date);
        
        // Just waiting for user input (disabled)
        print!("{}flux 1.0 >>> Input Disabled{}", RESET, RESET);
        io::stdout().flush().unwrap();
        
        let mut user_input = String::new();
        io::stdin().read_line(&mut user_input).unwrap();
        
        // Exit the loop if user types "exit"
        if user_input.trim().to_lowercase() == "exit" {
            println!("{}Exiting flux terminal...{}", RESET, RESET);
            break;
        }
    }
}
