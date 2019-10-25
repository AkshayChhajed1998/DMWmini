/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package stest;

import java.util.concurrent.TimeUnit;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
//import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 *
 * @author WorkStation
 */
public class Stest {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
          // declaration and instantiation of objects/variables
    	//System.setProperty("webdriver.firefox.marionette","C:\\geckodriver.exe");
		//WebDriver driver = new FirefoxDriver();
		//comment the above 2 lines and uncomment below 2 lines to use Chrome
	System.setProperty("webdriver.chrome.driver","C:\\chromedriver.exe");
	WebDriver driver = new ChromeDriver();
    	WebDriverWait wait = new WebDriverWait(driver,10);
        String baseUrl = "localhost:8000/";
        String expectedTitle = "HOME";
        String actualTitle = "";

        // launch Fire fox and direct it to the Base URL
        driver.get(baseUrl);
        actualTitle = driver.getTitle();
        WebElement apriori_a=driver.findElement(By.id("apriori_a"));
        apriori_a.click();
        WebElement select=driver.findElement(By.id("select"));
        select.sendKeys("Football");
        WebElement fetch = driver.findElement(By.id("fetch"));
        fetch.click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("table")));
        WebElement table =  driver.findElement(By.id("table")); 
        /*
         * compare the actual title of the page with the expected one and print
         * the result as "Passed" or "Failed"
         */
        if (table != null){
            System.out.println("Test 1 Passed!");
        } else {
            System.out.println("Test 1 Failed");
        }
        
        WebElement home_b = driver.findElement(By.id("home"));
        home_b.click();
        
        WebElement kmeans_a = driver.findElement(By.id("kmeans_a"));
        kmeans_a.click();
        
        WebElement type = driver.findElement(By.id("select"));
        type.sendKeys("Population");
        
        WebElement fetch_b = driver.findElement(By.id("button"));
        fetch_b.click();
        
        WebElement type1 = driver.findElement(By.id("select"));
        
        if( type1.getAttribute("value").equals("PopulationNorm"))
        {
            System.out.println("Test 2 Passed!");
        }
        else
        {
            System.out.println("Test 2 Failed!");
        }
        
        WebElement fig1;
        try{
            fig1 = driver.findElement(By.cssSelector("#fig1 div"));
        }
        catch(Exception e){
            fig1 = null;
        }
        
        if(fig1 != null)
        {
            System.out.println("Test 3 Passed!");
        }
        else
        {
            System.out.println("Test 3 Failed!");
        }
        
        WebElement fig2;
        try{
            fig2 = driver.findElement(By.cssSelector("#fig2 div"));
        }
        catch(Exception e){
            fig2 = null;
        }
        
        if(fig2 != null)
        {
            System.out.println("Test 4 Passed!");
        }
        else
        {
            System.out.println("Test 4 Failed!");
        }
        
         /*//Failing Tests
        WebElement fig1;
        try{
            fig1 = driver.findElement(By.cssSelector("#fig1 span"));
        }
        catch(Exception e){
            fig1 = null;
        }
        
        if(fig1 != null)
        {
            System.out.println("Test 3 Passed!");
        }
        else
        {
            System.out.println("Test 3 Failed!");
        }
        
        try{
            fig2 = driver.findElement(By.cssSelector("#fig2 span"));
        }
        catch(Exception e){
            fig2 = null;
        }
        
        WebElement fig2;
        if(fig2 != null)
        {
            System.out.println("Test 4 Passed!");
        }
        else
        {
            System.out.println("Test 4 Failed!");
        }
            
        */
        
        WebElement home_b1 = driver.findElement(By.id("home"));
        home_b1.click();
        
        if(driver.getTitle().equals("HOME"))
        {
            System.out.println("Test 5 Passed!");
        }
        else{
            System.out.println("Test 5 Failed!");
        }
        
       
        
        
        
        
        driver.close();
        
    }
    
}
