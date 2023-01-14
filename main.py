import requests
import csv
import json
import pandas as pd
import time

HEADERS = {
    "cookie": "ARRAffinity=5f9deab5efc3450516cafa1229ed550327e6434f153520c88607dcf184b1e44d; ARRAffinitySameSite=5f9deab5efc3450516cafa1229ed550327e6434f153520c88607dcf184b1e44d; .AspNetCore.Identity.Application=CfDJ8DZAA0_ocfxKkTgZsSWBni1_GyUMwWBVvsDXVI_7dzjffhY6GmYqVlLhUf1fdrMvwnGpbMae5ZDdIygoBrxfR7HjvFSbqMq3HYsKLyyjINTX2FWG8hYlx72Vf276wRfVcq1GFbv1iXLZ9f2RR53IMJjsj6IU3qF-Xy6_Vgdm8cz8jItjalmKd4afW01UMzAnwynlulqyH0emZikrHCITns7yBZW8qSzA0CPd2ajOIyTp2YBwF02AzpFVAgoGl9zHLqm0Va0H_XmJZcG9_1Rrl5-CDuMUbvxGNQXzNDI1sNmLaaD_AwaOHqchqDxtubrPOCWsH5o0mz9YBreL9l68-w9FmGA1zxxogb-EAPGAcmMfZI0SgxJ8afQSZ4ZfX8Vdb7tzaGXuivHvowKpg3p3ZDNw0wUv4bIFIB4NRCRKaKg5bF87EY2jThKUpGXYXCvgbIt8DQsdkFMh0Rihs8vk8VB9qR5_TZgSRMOPOz7vNhFzVeGUSW6y9rzc54qATgsI_59Pq0hxGw9iSqE93FF6A-amIcfIvoTSuD--Whqy8h6TyQUDX2CSzrYtbgzxWYZ5yexm8KnFwjHn0Fm98ojs4QvcjXugRywIL4dLrtCcW22YiNYB6CG2JlzjJ3feADI9JDeAHqFZRafb5qZ-wTth7xJEpPBYsBqi4mb2rtXkThFj4TBx5G-0-TGkFT1xBjKQJLFK_eFGzGDxDn3HhWU6m-Yka8OWrhR-Ku5iOfGvfLwsS3xQtkaHlw8hw_SlGo1dg1IvZKEhIUwcsTr0KVByKQfa7dHFGiCet3cyhBHfYDn0v_unlS_OZjSm6E1WDYcNTRk8agHyRVr6aT5pZFDBh7-iCnht8N0P9r7awM9_44gCGOVcq2ZL7CJqWNRXdMX_bMGlktSlAyW3cpW_cwJJarERle5XN-MvvUrijmpx1xkitet0L_p73zQreK2PdYAsMUgJ7uT6usjE3N4q9QVRgAROPeA4Okpa8ynQFeoLuyfndw2DZcPyjnhklUyGU0TvcLm_TCMY8eQ7WkgZxOZlZS1mz7ooJRmgGrWKg5lkqAHIhij7QLNfzKed2z-2c922F7b-r9M91nrH95OETK1y5_G3-IQUHIs035KQN316WqWiOq_kR_WrsL3hxpOoeOAbzQ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "apikey": "93b681cd0a37487f8f124adf603ce3bf",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkEyRUI2MzcyRDg4Rjk2MTI3QUI2QjJGMzBGOTc1N0ZBOUYxMjlEMThSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im91dGpjdGlQbGhKNnRyTHpENWRYLXA4U25SZyJ9.eyJuYmYiOjE2NzM1NDYyOTIsImV4cCI6MTY3MzU3NTA5MiwiaXNzIjoiaHR0cHM6Ly9wb3AueHByaXplLm9yZyIsImF1ZCI6WyJYUFBPUEFQSSIsImh0dHBzOi8vcG9wLnhwcml6ZS5vcmcvcmVzb3VyY2VzIl0sImNsaWVudF9pZCI6IlBPUC1NVkMiLCJzdWIiOiI0ZDdjOWIxNy0yMGI1LTQ2ZWMtYTY3My0xMTQ0MGJkMGQ0YTQiLCJhdXRoX3RpbWUiOjE2NzM1NDYyOTIsImlkcCI6ImxvY2FsIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoibWNmdXJsYW5kQGdtYWlsLmNvbSIsIkFzcE5ldC5JZGVudGl0eS5TZWN1cml0eVN0YW1wIjoiQlY3UTVEVFkzTzdSSFZLRlZGQ1VLVEw1VlNPQ0NSV1EiLCJlbWFpbCI6Im1jZnVybGFuZEBnbWFpbC5jb20iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtY2Z1cmxhbmRAZ21haWwuY29tIiwibmFtZSI6Im1jZnVybGFuZEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwic2lkIjoiMEU1NDk0QjU1NzlGMDBEMDk3QTY1OTVGMTRFOTk0RjMiLCJpYXQiOjE2NzM1NDYyOTIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJlbWFpbCIsIlhQUE9QQVBJIl0sImFtciI6WyJwd2QiXX0.IPWInkB5jQ02rDtTQ-0Hf0DI13eaqQRc9R3RgZrIywgaDaRBeM0lncuIq_yTqsogjPFHUqNsYEv0L9hbsbEiLcmntPNTDA0VBB13_VCSsFJxXw75dwdZqfAko_tzvMRknhyP40_8FUjQ4sVHYH9zBGHm6GBcxBE60lieqDB-0xGhBJxhdrK-xQJaKo0H0dSadGNmDzOjk0YVcUHLWCm-9VE4mDlu9VQM2EM4CC8IQDWbB6VxN-CaxRntrBUdPeBzjKul5IzT_H6WDSryuj37Ft0DgeJ3_AqRO2VuhP7ZQ3fKKS5np0kJvn4Mw1kzRsA9kzWaIR1KXUHhnnA82bZaFA",
    "Connection": "keep-alive",
    "Referer": "https://pop.xprize.org/teams/736/overview",
    "Cookie": "_ga=GA1.2.1087725601.1673288554; _gid=GA1.2.840636183.1673288554; _fbp=fb.1.1673288554825.955206787; cookieconsent_status=dismiss; ARRAffinity=bd0a89aab23ce188a74690df51a5092ac432ddeb109c4f823d89229b2db163eb; ARRAffinitySameSite=bd0a89aab23ce188a74690df51a5092ac432ddeb109c4f823d89229b2db163eb; .AspNetCore.Identity.Application=CfDJ8DZAA0_ocfxKkTgZsSWBni3SUVRIuH0ev474K-Hm5D45672L32bwgnJwi4zW4DBK6k3kP45iEVc6o8Ii-MX9YRAxjAXB7YxpnRDjbFwtRBnmGBvhwdy-oYou2y7Xh0MZbCUy0e4C1wtcSbVyX8u14Z9feqU8LbBWsOOCRwmktr3pwJ2VguYY1Xm5oH_IGk9b3wNTfybxNfeWJ4uoFmobHgOZQ3sW2lv_qK9Psm6DA0oFef2gMg_QhEAdsJAhAP_pOXD0X611Xbzly4miP-94KGAWoWmGfS2No4Dl38Csc1M0Qr3JMgEskhi1CjNyGVOKeQezW9rbwx8Wg0WQf18HJwEPxBda7_BGwlGCtPnjzwmJhsI55C0XqnYL-BAvmEvrbGGD2AN-1dhBUVcbsAxjdj0sXM55oDJaCRgb5TP7qKjTOzXSUvkBhRW9auRIky0WTdqxoEpmhi3YxJS05WhOsT0hntMPa9IT7v47xGyVIzLZXH-eijPgjYUFoGIyH77s1ou2JhEQnDrRFFf0ZIFJisEI4uzuYoCUmkqfeYE1MhKrb9HUz1YSW5L81UB2pXsX7ByJb6loV4FoZIMoo1SmOmEy5zrdaC72AhowI3_tRKMM0OA9B855ukt4xrSCLdgRqPmQx79A9RKfjUHGExl8TXpF2gHGkicTLU76KwQQQAIVRMBaalpDWP7segIWGz9r-lZCsyTY8YJ2jdl91vYPVy2QruiPnd7fsvTWEkzsndCXS_XxEBXAIot-MSUa2SnvOmC73I2sO0y8ucGEuBPYaOyWMINZFS3dFc_Gg4kkdXfAyZIaYz8V7srfbTlzCE7_3PQ1alum2RP4tFnwuIIVTgkNRvzKAJaRuR0xsL9wvkBtUBp0HnzOibgIyjVOzKBvxXhYMXl3kiF-uP64Rbvnnhhpcw6ZqzUjNhYsd6XeHE5xNUBuP3DeMOk4Zie-qvvy2wLi7ztm6k8bJ6zgeTb1Js6VmCK4YZWEIWoQ3Mw8UL7KaWFW8l612f8o9Gg_hGnrgTQyd-HWHzbKllSxBHz788zpK5Jbbdh2KVv0itsrb2DJZfclaHITAf5GMOKVof6uHZx_kL5qDcQlUSFWRZffczDRQtBnu5eU8HR0_RDgJAPUmQ2E_PIXoZz2fkgNSkL1Qg; idsrv.session=0E5494B5579F00D097A6595F14E994F3",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}
TEAM_HEADER = {
    "cookie": "_ga=GA1.2.1834178678.1672940560; _fbp=fb.1.1672940560249.600701882; _ju_dn=1; _ju_dc=b71587e4-b78a-11ec-9af6-21fbf060664c; cookieconsent_status=dismiss; _gid=GA1.2.1040929841.1673411717; _ju_dm=cookie; ARRAffinity=5f9deab5efc3450516cafa1229ed550327e6434f153520c88607dcf184b1e44d; ARRAffinitySameSite=5f9deab5efc3450516cafa1229ed550327e6434f153520c88607dcf184b1e44d; idsrv.session=C68519DC6CD45F2263BF40E6B376A435; .AspNetCore.Identity.Application=CfDJ8HgFnF8-H5RCigfSVjzTLZ2sVi4GcnSCTE7Dz_Zq8m1TjxZCgNTZsUAGYYbTDK1kPBCs1ZK_pviIqwCS7IVHq-piKQeq_YT-NJ-zWDgHX4vImhLZVci6M8qviDvnn43Oue4REcdHjpOY18lp0ZdKXPOEPk2fQqIz4HADzcGwHM_i-jobb3dCArRMYC8kIKKLBY-yHEeumKULLQoHBOCW3_f3tGThtPvt5Meza-LibDYnUs9hY7GsHc06zOHmVZokwKjz_ZbtJ3tD5MerEBGTE8R8w9xE6erUlnrgbdzen_0BAXoGtB68jyAmoPxAKWbWlz9q11TrSwvw_JTnBH1O5hronPdPVv4cX4YyjwZMTRPNTgYY0Ybjke98oTXN2chfKkZT1cQJGET-FF11C7yroM5PXH3tV7snmGr07DLwEXqQWQaBmMEacpaBpJ8wPwaO69Nd-QPAlvPWC_4JL875IrG7lqbX7i50VAr_scULc9iRh-9Cdda2sarmgkYcxHlqTm79ir99n8ondqajz_h8x8wEaIweTQG4OMFuNJnZZ9zU6pYJ9r7zcbEL1XOmu0BJnygJuWqABZwcaySzBRfIaNos-QToMV2z3b8TVFsLfaxrV5CQRodqKX30sBZVJH2bnjsj309pVldlxEf7oa7KjCf1K_ry4FpmhUZhYKqMlcXYOkr8mInxPhLgaNhCCss0YNCXYzPla_flmHWid_0IbhQNlyRjTTh41zw2bflgoUwywP3U4yQ9bHc7K8TqzOaERmpCr_YNx8sotMdQGLUJUqQtUSRuCi4c6RyvlW-OMLQWIdQYZ6djZox_W3Oh5NApQ8EZ6_6cjN9QCrTmC49w22DgBiYRBq8t1lW_pZaIMaQPmbN9KP2I0uJO3Y7m0xkobDL93L5r2RR9ebF3_Do-9VthY2vjZ7P8VqeXrYeX-XYVgp4wS8sj9O1bHLcj8wBj9K7wF7P7juL4z0L0udSYWEUyiAxt1RWOELgWx8GEu4lnW2SRs5i2TSY0sVT-JdEhzIxKsa1m48u3KkLF3-ZRa65ZVt7p9XilJ4-5N_R6zD5kk8vUUjdMhD9IFaUC70MLEcs5jI9vnlZuC3mY_q8ZkY77AkGS_hcBq4zUmBSiPD49UQf7kdp5wWP65ol1yQLrJg",
    "authority": "pop.xprize.org",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "apikey": "93b681cd0a37487f8f124adf603ce3bf",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkEyRUI2MzcyRDg4Rjk2MTI3QUI2QjJGMzBGOTc1N0ZBOUYxMjlEMThSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im91dGpjdGlQbGhKNnRyTHpENWRYLXA4U25SZyJ9.eyJuYmYiOjE2NzM2MzkxMDIsImV4cCI6MTY3MzY2NzkwMiwiaXNzIjoiaHR0cHM6Ly9wb3AueHByaXplLm9yZyIsImF1ZCI6WyJYUFBPUEFQSSIsImh0dHBzOi8vcG9wLnhwcml6ZS5vcmcvcmVzb3VyY2VzIl0sImNsaWVudF9pZCI6IlBPUC1NVkMiLCJzdWIiOiI0ZDdjOWIxNy0yMGI1LTQ2ZWMtYTY3My0xMTQ0MGJkMGQ0YTQiLCJhdXRoX3RpbWUiOjE2NzM2MzkxMDAsImlkcCI6ImxvY2FsIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoibWNmdXJsYW5kQGdtYWlsLmNvbSIsIkFzcE5ldC5JZGVudGl0eS5TZWN1cml0eVN0YW1wIjoiQlY3UTVEVFkzTzdSSFZLRlZGQ1VLVEw1VlNPQ0NSV1EiLCJlbWFpbCI6Im1jZnVybGFuZEBnbWFpbC5jb20iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtY2Z1cmxhbmRAZ21haWwuY29tIiwibmFtZSI6Im1jZnVybGFuZEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwic2lkIjoiQzY4NTE5REM2Q0Q0NUYyMjYzQkY0MEU2QjM3NkE0MzUiLCJpYXQiOjE2NzM2MzkxMDIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJlbWFpbCIsIlhQUE9QQVBJIl0sImFtciI6WyJwd2QiXX0.UOvQOCNBQ42vCnkGcTfmtLywZWLQDm_3JE6Cx-8nuAPTLiJd7xKc47CIS4R1bGCyi3GsmlsRvoU42ftzo_xE3x8ZkcJ_GeRe6V8v0QVLRjX30cpvit5fKYT-ffPTBcY3MijxszTC67wZSwkogYAEdR1VwgEOMO0fiY_6vD1aFFFXWqKo-Ztl8woA4Gy_dU_QIDpOPFrnEitZz-uJ9wRUsLFIODg_zVCR--3kJtoflVGb8rMalf9YpehEkXbSEnlkaaJtdKNg3JvBDg-tIq0vUimNrItVygkjYgTnZo0G_5oot9RYXb15vf1ilhhE87YV1u8lJNsh0AFw05Qg6K9eaA",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://pop.xprize.org/teams/5220/overview",
    "sec-ch-ua": "^\^Not?A_Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^108^^, ^\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
TEAM_HEADER2 = {
    "cookie": "_ga=GA1.2.1834178678.1672940560; _fbp=fb.1.1672940560249.600701882; _ju_dn=1; _ju_dc=b71587e4-b78a-11ec-9af6-21fbf060664c; cookieconsent_status=dismiss; _gid=GA1.2.1040929841.1673411717; _ju_dm=cookie; ARRAffinity=5f9deab5efc3450516cafa1229ed550327e6434f153520c88607dcf184b1e44d; ARRAffinitySameSite=5f9deab5efc3450516cafa1229ed550327e6434f153520c88607dcf184b1e44d; idsrv.session=C68519DC6CD45F2263BF40E6B376A435; .AspNetCore.Identity.Application=CfDJ8HgFnF8-H5RCigfSVjzTLZ2sVi4GcnSCTE7Dz_Zq8m1TjxZCgNTZsUAGYYbTDK1kPBCs1ZK_pviIqwCS7IVHq-piKQeq_YT-NJ-zWDgHX4vImhLZVci6M8qviDvnn43Oue4REcdHjpOY18lp0ZdKXPOEPk2fQqIz4HADzcGwHM_i-jobb3dCArRMYC8kIKKLBY-yHEeumKULLQoHBOCW3_f3tGThtPvt5Meza-LibDYnUs9hY7GsHc06zOHmVZokwKjz_ZbtJ3tD5MerEBGTE8R8w9xE6erUlnrgbdzen_0BAXoGtB68jyAmoPxAKWbWlz9q11TrSwvw_JTnBH1O5hronPdPVv4cX4YyjwZMTRPNTgYY0Ybjke98oTXN2chfKkZT1cQJGET-FF11C7yroM5PXH3tV7snmGr07DLwEXqQWQaBmMEacpaBpJ8wPwaO69Nd-QPAlvPWC_4JL875IrG7lqbX7i50VAr_scULc9iRh-9Cdda2sarmgkYcxHlqTm79ir99n8ondqajz_h8x8wEaIweTQG4OMFuNJnZZ9zU6pYJ9r7zcbEL1XOmu0BJnygJuWqABZwcaySzBRfIaNos-QToMV2z3b8TVFsLfaxrV5CQRodqKX30sBZVJH2bnjsj309pVldlxEf7oa7KjCf1K_ry4FpmhUZhYKqMlcXYOkr8mInxPhLgaNhCCss0YNCXYzPla_flmHWid_0IbhQNlyRjTTh41zw2bflgoUwywP3U4yQ9bHc7K8TqzOaERmpCr_YNx8sotMdQGLUJUqQtUSRuCi4c6RyvlW-OMLQWIdQYZ6djZox_W3Oh5NApQ8EZ6_6cjN9QCrTmC49w22DgBiYRBq8t1lW_pZaIMaQPmbN9KP2I0uJO3Y7m0xkobDL93L5r2RR9ebF3_Do-9VthY2vjZ7P8VqeXrYeX-XYVgp4wS8sj9O1bHLcj8wBj9K7wF7P7juL4z0L0udSYWEUyiAxt1RWOELgWx8GEu4lnW2SRs5i2TSY0sVT-JdEhzIxKsa1m48u3KkLF3-ZRa65ZVt7p9XilJ4-5N_R6zD5kk8vUUjdMhD9IFaUC70MLEcs5jI9vnlZuC3mY_q8ZkY77AkGS_hcBq4zUmBSiPD49UQf7kdp5wWP65ol1yQLrJg",
    "authority": "pop.xprize.org",
    "accept": "application/json, text/plain, */*",
    "content-type": "charset=utf-8",
    "accept-language": "en-US,en;q=0.9",
    "apikey": "93b681cd0a37487f8f124adf603ce3bf",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkEyRUI2MzcyRDg4Rjk2MTI3QUI2QjJGMzBGOTc1N0ZBOUYxMjlEMThSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im91dGpjdGlQbGhKNnRyTHpENWRYLXA4U25SZyJ9.eyJuYmYiOjE2NzM2MzkxMDIsImV4cCI6MTY3MzY2NzkwMiwiaXNzIjoiaHR0cHM6Ly9wb3AueHByaXplLm9yZyIsImF1ZCI6WyJYUFBPUEFQSSIsImh0dHBzOi8vcG9wLnhwcml6ZS5vcmcvcmVzb3VyY2VzIl0sImNsaWVudF9pZCI6IlBPUC1NVkMiLCJzdWIiOiI0ZDdjOWIxNy0yMGI1LTQ2ZWMtYTY3My0xMTQ0MGJkMGQ0YTQiLCJhdXRoX3RpbWUiOjE2NzM2MzkxMDAsImlkcCI6ImxvY2FsIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoibWNmdXJsYW5kQGdtYWlsLmNvbSIsIkFzcE5ldC5JZGVudGl0eS5TZWN1cml0eVN0YW1wIjoiQlY3UTVEVFkzTzdSSFZLRlZGQ1VLVEw1VlNPQ0NSV1EiLCJlbWFpbCI6Im1jZnVybGFuZEBnbWFpbC5jb20iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtY2Z1cmxhbmRAZ21haWwuY29tIiwibmFtZSI6Im1jZnVybGFuZEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwic2lkIjoiQzY4NTE5REM2Q0Q0NUYyMjYzQkY0MEU2QjM3NkE0MzUiLCJpYXQiOjE2NzM2MzkxMDIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJlbWFpbCIsIlhQUE9QQVBJIl0sImFtciI6WyJwd2QiXX0.UOvQOCNBQ42vCnkGcTfmtLywZWLQDm_3JE6Cx-8nuAPTLiJd7xKc47CIS4R1bGCyi3GsmlsRvoU42ftzo_xE3x8ZkcJ_GeRe6V8v0QVLRjX30cpvit5fKYT-ffPTBcY3MijxszTC67wZSwkogYAEdR1VwgEOMO0fiY_6vD1aFFFXWqKo-Ztl8woA4Gy_dU_QIDpOPFrnEitZz-uJ9wRUsLFIODg_zVCR--3kJtoflVGb8rMalf9YpehEkXbSEnlkaaJtdKNg3JvBDg-tIq0vUimNrItVygkjYgTnZo0G_5oot9RYXb15vf1ilhhE87YV1u8lJNsh0AFw05Qg6K9eaA",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://pop.xprize.org/teams/5220/overview",
    "sec-ch-ua": "^\^Not?A_Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^108^^, ^\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
TEAM_URL = "https://pop.xprize.org/api/Teams/"


# TODO: #1. Retrieve all "TeamId" from endpoint http://pop.xprize.org/api/Prizes/xprize_carbon_capture/teams, changing
#  query parameter to max number of teams that signed up for $100M Carbon Capture Comp.
# wanted to have get_team_id return a list of all the team_id that I could pass through get_basic_team_info()


def get_team_id():
    r = requests.get("http://pop.xprize.org/api/Prizes/xprize_carbon_capture/teams?offset=0&limit=5088",
                     headers=HEADERS).json()

    # Keep this commented out unless you want to make a new text file with all team id
    with open("txt_and_csv_files/team_id_list.txt", "a") as file:
        for team in r["Result"]:
            team_id = str(team["TeamId"])
            file.write(f"{team_id}\n")

    team_id_list = []
    for team in r["Result"]:
        team_id_list.append(team["TeamId"])

    return team_id_list


def extract_team_info(id_list):
    # with open("text_docs/team_id_list.txt") as file:
    #     for team in file:
    #         team = team.strip("\n")
    s = requests.Session()
    remaining = 5088
    for team in id_list:
        r = s.get(f"{TEAM_URL}{team}", headers=TEAM_HEADER2).text
        team_json_file = json.loads(r)
        team_id = team_json_file["Result"]["TeamId"]
        team_name = team_json_file["Result"]["TeamName"]
        team_fb_account = team_json_file["Result"]["FacebookAccount"]
        team_linkedin_account = team_json_file["Result"]["LinkedInAccount"]
        team_twitter_account = team_json_file["Result"]["TwitterAccount"]
        primary_phone_number = team_json_file["Result"]["PhoneNumber"]
        team_bio = team_json_file["Result"]["About"]
        team_country = team_json_file["Result"]["Country"]
        team_city = team_json_file["Result"]["City"]
        team_websites = []
        for _ in team_json_file["Result"]["TeamWebsites"]:
            team_websites.append(_["Website"])

        all_team_data.append((team_id, team_name, team_fb_account, team_linkedin_account, team_twitter_account,
                              primary_phone_number, team_country, team_city, team_bio, team_websites))
        remaining -= 1
        print(f"{team} completed. remaining: {remaining}")


def team_info_to_csv():
    # df = pd.read_csv("txt_and_csv_files/team_info.csv")
    df = pd.DataFrame(all_team_data)
    df.columns = ["Team Id", "Team Name", "Facebook", "LinkedIn", "Twitter", "Phone Number", "Country", "City", "Bio",
                  "Websites"]
    df["Websites"] = df["Websites"].replace("[]", "")
    df.to_csv("txt_and_csv_files/team_info.csv", index=False)


# Needs to be run a couple of times. Once the script encounters JSONDecodeError, it will display the "team id" that
# failed. At this point, go to "team_id_list.txt" and delete all team_id's above failed id. Run again
def get_basic_user_data():
    completed = 0
    s = requests.Session()

    with open("txt_and_csv_files/team_id_list.txt") as file:
        for team in file:
            team = team.strip("\n")
            r = s.get(f"https://pop.xprize.org/api/Teams/{team}/members", headers=HEADERS).text
            while True:
                try:
                    r_json = json.loads(r)
                except json.decoder.JSONDecodeError:
                    print(f"team {team} failed")
                    time.sleep(15)
                    continue
                else:
                    for member in r_json["Result"]:
                        user_id = member["UserId"]
                        full_name = member["FullName"]
                        email = member["Email"]
                        team_id = member["TeamMembers"][0]["TeamId"]
                        basic_team_data = (user_id, team_id, full_name, email)
                        completed += 1
                        print(f"{completed} members added")
                        with open("txt_and_csv_files/basic_user_data.csv", "a", newline='', encoding="utf-8") as f:
                            csvwriter = csv.writer(f)
                            csvwriter.writerow(basic_team_data)
                        with open("txt_and_csv_files/member_id_list.txt", "a") as f:
                            f.write(f"{user_id}\n")
                break


# Needs to be run a couple of times. Once the script encounters JSONDecodeError, it will display the "user id" that
# failed. At this point, go to "member_id_list.txt" and delete all member_id's above failed id. Run again
def get_detailed_user_data():
    completed = 0
    s = requests.Session()

    with open("txt_and_csv_files/member_id_list.txt") as file:
        for count, unique_id in enumerate(file):
            pass
    with open("txt_and_csv_files/member_id_list.txt") as file:
        for unique_id in file:
            unique_id = unique_id.strip("\n")

            while True:
                try:
                    response = s.get(url=f"https://pop.xprize.org/api/User/Profile/{unique_id}",
                                     headers=TEAM_HEADER2).json()
                except requests.exceptions.JSONDecodeError:
                    print(f"{unique_id} failed")
                    time.sleep(15)
                    continue
                else:
                    degrees = []
                    universities = []
                    skills = []
                    websites = []
                    bio = response["Result"]["Profile"]["About"]
                    facebook = response["Result"]["Profile"]["Fbaccount"]
                    linkedin = response["Result"]["Profile"]["LinkedInAccount"]
                    google_plus = response["Result"]["Profile"]["GooglePlusAccount"]
                    twitter = response["Result"]["Profile"]["TwitterAccount"]
                    city = response["Result"]["Profile"]["City"]
                    for _ in response["Result"]["UserEducation"]:
                        degrees.append(_["Degree"])
                        universities.append(_["University"])
                    for _ in response["Result"]["Websites"]:
                        websites.append(_["Website"])
                    for _ in response["Result"]["Skills"]:
                        skills.append(_["Skill"]["SkillName"])

                    user_profile = (unique_id, bio, facebook, linkedin, google_plus, twitter, city, websites, degrees,
                                    universities, skills)
                    completed += 1
                    print(f"{completed}/{count + 1} completed")
                    with open("txt_and_csv_files/detailed_user_data.csv", "a", encoding="utf-8", newline='') as f:
                        csvwriter = csv.writer(f)
                        csvwriter.writerow(user_profile)
                    # if completed % 1000 == 0:
                    #     time.sleep(90)
                break


def convert_to_excel():
    df1 = pd.read_csv("txt_and_csv_files/basic_user_data.csv")
    df1.columns = ["User ID", "Team ID", "Name", "Email"]
    df1.set_index("User ID", inplace=True, drop=True)

    df2 = pd.read_csv("txt_and_csv_files/detailed_user_data.csv")
    df2.columns = ["User ID", "Bio", "Facebook", "LinkedIn", "Google Plus", "Twitter", "City", "Websites", "Degrees",
                   "Universities", "Skills"]
    df2.set_index("User ID", inplace=True, drop=True)

    joined_df = df1.join(df2)
    joined_df.to_csv("finished_product.csv")
    print(joined_df)


all_team_data = []

# team_id_list = get_team_id()
# extract_team_info(team_id_list)
# get_basic_user_data()
# get_detailed_user_data()
# convert_to_excel()
