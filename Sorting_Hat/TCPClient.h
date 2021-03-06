#ifndef __TCPClient_h__
#define __TCPClient_h__


/* Windows DLL */
#ifdef XP_WIN
# define OSCALL __stdcall
#else
# define OSCALL 
#endif

#ifdef __cplusplus
extern "C" {
#endif 

/*
 Create browser instance.
 The function starts browser if no browser process is started, otherwise
 a new browser window is created.

 @browser - "cr" for Google Chrome, "fx" for Firefox
 @options - extra options string, like -fxProfile
 @binary_location - path for non-default binary location
 @port - optional port number, use 0 for pipes, -1 for default port number
 @openNewBrowser - 0 for false, any other value for true, if true - opens new
    browser window for every iimInit()
 @timeout - timeout for starting browser, set -1 for default value

 returns 0 or negative error code
*/
int OSCALL im_Init(const char* browser, const char* options,
                   const char* binary_location, int port,
                   int openNewBrowser, int timeout);

typedef int (OSCALL *im_Init_t)
    (const char* browser, const char* options,
     const char* binary_location, int port,
     int openNewBrowser, int timeout);

/*
  Close browser window
  @timeout - optional timeout value in sec, 0 for default value
*/
int OSCALL im_Exit(int timeout);

typedef int (OSCALL *im_Exit_t)(int timeout);


/*
  Set variable for current instance.
  Should be reset before every im_Play() call.

  @var_name - variable name
  @var_value - variable value

  returns 0 or negative error code
*/
int OSCALL im_SetVar(const char* var_name, const char* var_value);

typedef int (OSCALL *im_SetVar_t)
        (const char* var_name, const char* var_value);


/*
  Play specified macro

  @name_or_code - name of macro in macros folder, path to a macro, macro code
  @timeout - timeout for macro replay, 0 for default value (600s)

  returns 0 or negative error code
*/

int OSCALL im_Play(const char* name_or_code, int timeout);

typedef int (OSCALL *im_Play_t)(const char* name_or_code, int timeout);


/*
  Shows @message in dialog box generated by browser
  @timeout - optional timeout value in sec,  0 for default value
*/
int OSCALL im_Display(const char *message, int timeout);

typedef int (OSCALL *im_Display_t)(const char *message, int timeout);


/*
  Returns content of !EXTRACT variable

  @buf - character buffer to store extracted string into, place NULL if
     you want to know required buffer size
  @buf_size - size of the buffer (should have place for terminating 0)
  @index - index of extracted text portion, 0 for whole extraction

  returns number of bytes written (including terminating 0 character) or
  negative value if buffer size is not enough
*/
int OSCALL im_GetLastExtract(char *buf, int buf_size, int index);

typedef int (OSCALL *im_GetLastExtract_t)
    (char *buf, int buf_size, int index);


/*
  Get error text

  @buf - character buffer to store extracted string into, place NULL if
     you want to know required buffer size
  @buf_size - size of the buffer (should have place for terminating 0)

  returns number of bytes written (including terminating 0 character) or
  negative value if buffer size is not enough
*/
int OSCALL im_GetLastErrorText(char *buf, int buf_size);

typedef int (OSCALL *im_GetLastErrorText_t)(char *buf, int buf_size);


/*
  Get numeric error code
*/
int OSCALL im_GetLastErrorNumber();

typedef int (OSCALL *im_GetLastErrorNumber_t)();


/*
 Take Browser screenshot
  @path - path to file (note, only png files allowed)
  @type - 1 for web-page screenshot, 0 - browser screenshot (not supported yet)
  @timeout - optional timeout value in sec,  0 for default value

  returns 0 in success or negative value in case of error
*/
int OSCALL im_TakeBrowserScreenshot(const char* path, int type, int timeout);
typedef int (OSCALL *im_TakeBrowserScreenshot_t)(const char* path,
                                                 int type,
                                                 int timeout);


/*
Returns the data of the STOPWATCH command. If there is no STOPWATCH command in the macro then iimGetLastPerformance returns only one value ("Total Runtime").

 in    @idx - 1 for total runtime, 2, 3.. for next STOPWATCH data
 out   @name - buffer for value name, optional if idx=1, if set to NULL
the required buffer size including terminating \0 is returned in name_size.
 inout @name_size - buffer size, if @name is NULL then required size is
returned, otherwise returns the number of bytes written (without terminating \0)
 out   @value - buffer for value data, usage is the same as @name
 inout @value_size - value buffer size, usage is the save as @name_size

returns 0 in success, -1 if no data available or some error occurred,
  -2 - buffer size is not enough
*/
int OSCALL im_GetLastPerformance(int idx, char *name, int *name_size,
                                 char *value, int *value_size);

typedef int (OSCALL *im_GetLastPerformance_t)(int idx,
                                              char *name, int *name_size,
                                              char *value, int *value_size);

#ifdef __cplusplus
}
#endif 


#endif  /* __TCPClient_h */
