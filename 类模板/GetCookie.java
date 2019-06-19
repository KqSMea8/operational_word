package Util;

import java.io.IOException;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.CookiePolicy;
import java.net.CookieStore;
import java.net.HttpCookie;
import java.net.URL;
import java.net.URLDecoder;
import java.util.HashMap;
import java.util.List;
import java.util.logging.Handler;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;

import org.testng.Assert;
import org.testng.annotations.Test;


import com.alibaba.fastjson.JSONObject;
import com.bj58.daojia.qa.base.BaseTest;
import com.bj58.daojia.qa.http.HttpRequest;

public class GetCookie {
    String InpassUrl="http://inpass.daojia-inc.com/user/login";
    @Test
	public String getCookieResult() throws IOException {
		  final String userName="";
		  final String password="";
		  final String redirect="http://djoy.daojia-inc.com/";
		  final String UserAgent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36";
		        String Cookies="";
		    try
		    {

		        JSONObject result = HttpRequest.doPostReturnResponseJson(InpassUrl,
		            new HashMap<String, String>() {
		                {
		                	put("userName",userName);
		                	put("password",password);
		                	put("redirect",redirect);
		                }
		            }, new HashMap<String, String>() {
		                {
		                	put("User-Agent", UserAgent );
		    			
		                }
		            });
		//  System.out.println(result.getJSONArray("cookies"));
		  com.alibaba.fastjson.JSONArray tempCookies = result.getJSONArray("cookies");
		  Cookies= tempCookies.getJSONObject(0).getString("name")+"="+
		           tempCookies.getJSONObject(0).getString("value")+";"+
		   	  	  tempCookies.getJSONObject(1).getString("name")+"="+
		          tempCookies.getJSONObject(1).getString("value");
		//  System.out.println(Cookies);   	
	    }	
		    catch(Exception e)
			 {
				 Assert.fail("Cookies获取失败");
				 e.printStackTrace(); 
			 }		
		  return Cookies;
	 }
    
  /*  
    @Test
    public void getCookieResult1(){
    	try{
    		CookieManager manager=new CookieManager();
    		manager.setCookiePolicy(CookiePolicy.ACCEPT_ALL);
    		CookieHandler.setDefault(manager);
    		URL	url=new URL("http://inpass.daojia-inc.com/user/login");
    		HttpURLConnection conn = (HttpURLConnection)url.openConnection();  */
    	/*	conn.setRequestMethod("POST");	
    		String cookie = conn.getHeaderField("set-cookie");
    		System.out.println(cookie);
    		*/
    	/*
    		conn.getHeaderFields();
    		CookieStore store = manager.getCookieStore();
    		
    		List<HttpCookie> lCookies=store.getCookies();
    		System.out.printf("共%s个cookie\n",lCookies.size());
    		for (HttpCookie cookie: lCookies) {
    			System.out.printf("原:%s  名称:%s  解码值:%s\n", 
    				cookie.toString(),
    				cookie.getName(),
    				URLDecoder.decode(cookie.getValue(), "UTF8")); 
    		} 
    	}catch (Exception e){
    		
    		e.printStackTrace();
    	}
    }
    */
}
