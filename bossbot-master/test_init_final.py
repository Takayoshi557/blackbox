# -*- coding: utf-8 -*-

################ Server V16.6 (Japanese) #####################

import os
import sys
import asyncio
import discord
import datetime
import random
import math
import logging
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from gtts import gTTS
from github import Github
import base64
import re #정산
import gspread #정산
from oauth2client.service_account import ServiceAccountCredentials #정산
from io import StringIO
import urllib.request
from math import ceil, floor

##################### 로깅 ###########################
log_stream = StringIO()
logging.basicConfig(stream=log_stream, level=logging.WARNING)

#ilsanglog = logging.getLogger('discord')
#ilsanglog.setLevel(level = logging.WARNING)
#handler = logging.StreamHandler()
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#ilsanglog.addHandler(handler)
#####################################################

basicSetting = []
bossData = []
fixed_bossData = []

bossNum = 0
fixed_bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

fixed_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
fixed_bossFlag = []
fixed_bossFlag0 = []
bossMungFlag = []
bossMungCnt = []
bossMungTime = []
bossAutoMungCnt = []
bossAutoMungTime = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

FixedBossDateData = []
indexFixedBossname = []

client = discord.Client()
client = commands.Bot(command_prefix="", help_command = None, description='KuberaBot')

access_token = os.environ["BOT_TOKEN"]
git_access_token = os.environ["GIT_TOKEN"]
git_access_repo = os.environ["GIT_REPO"]
git_access_repo_restart = os.environ["GIT_REPO_RESTART"]

g = Github(git_access_token)
repo = g.get_repo(git_access_repo)
repo_restart = g.get_repo(git_access_repo_restart)

def init():
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt
	global bossMungTime
	global bossAutoMungCnt
	global bossAutoMungTime

	#voice:global voice_client1

	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	global LoadChk

	global indexFixedBossname
	global FixedBossDateData

	global endTime

	global gc #정산
	global credentials #정산

	global regenembed
	global command

	global tmp_racing_unit

	command = []
	tmp_bossData = []
	tmp_fixed_bossData = []
	FixedBossDateData = []
	indexFixedBossname = []
	f = []
	fb = []
	fk = []
	fc = []
	tmp_racing_unit = []

	inidata = repo.get_contents("test_setting.ini")
	file_data1 = base64.b64decode(inidata.content)
	file_data1 = file_data1.decode('utf-8')
	inputData = file_data1.split('\n')

	command_inidata = repo.get_contents("command.ini")
	file_data4 = base64.b64decode(command_inidata.content)
	file_data4 = file_data4.decode('utf-8')
	command_inputData = file_data4.split('\n')

	boss_inidata = repo.get_contents("boss.ini")
	file_data3 = base64.b64decode(boss_inidata.content)
	file_data3 = file_data3.decode('utf-8')
	boss_inputData = file_data3.split('\n')

	fixed_inidata = repo.get_contents("fixed_boss.ini")
	file_data2 = base64.b64decode(fixed_inidata.content)
	file_data2 = file_data2.decode('utf-8')
	fixed_inputData = file_data2.split('\n')

	for i in range(len(fixed_inputData)):
		FixedBossDateData.append(fixed_inputData[i])

	index_fixed = 0

	for value in FixedBossDateData:
		if value.find('bossname') != -1:
			indexFixedBossname.append(index_fixed)
		index_fixed = index_fixed + 1

	for i in range(inputData.count('\r')):
		inputData.remove('\r')

	for i in range(command_inputData.count('\r')):
		command_inputData.remove('\r')

	for i in range(boss_inputData.count('\r')):
		boss_inputData.remove('\r')

	for i in range(fixed_inputData.count('\r')):
		fixed_inputData.remove('\r')

	del(command_inputData[0])
	del(boss_inputData[0])
	del(fixed_inputData[0])

	############## 보탐봇 초기 설정 리스트 #####################
	basicSetting.append(inputData[0][11:])     #basicSetting[0] : timezone
	basicSetting.append(inputData[6][15:])     #basicSetting[1] : before_alert
	basicSetting.append(inputData[8][10:])     #basicSetting[2] : mungChk
	basicSetting.append(inputData[7][16:])     #basicSetting[3] : before_alert1
	basicSetting.append(inputData[11][14:16])  #basicSetting[4] : restarttime 시
	basicSetting.append(inputData[11][17:])    #basicSetting[5] : restarttime 분
	basicSetting.append(inputData[1][15:])     #basicSetting[6] : voice채널 ID
	basicSetting.append(inputData[2][14:])     #basicSetting[7] : text채널 ID
	basicSetting.append(inputData[3][16:])     #basicSetting[8] : 사다리 채널 ID
	basicSetting.append(inputData[10][14:])     #basicSetting[9] : !ㅂ 출력 수
	basicSetting.append(inputData[14][11:])    #basicSetting[10] : json 파일명
	basicSetting.append(inputData[4][17:])     #basicSetting[11] : 정산 채널 ID
	basicSetting.append(inputData[13][12:])    #basicSetting[12] : sheet 이름
	basicSetting.append(inputData[12][16:])    #basicSetting[13] : restart 주기
	basicSetting.append(inputData[15][12:])    #basicSetting[14] : 시트 이름
	basicSetting.append(inputData[16][12:])    #basicSetting[15] : 입력 셀
	basicSetting.append(inputData[17][13:])    #basicSetting[16] : 출력 셀
	basicSetting.append(inputData[9][13:])     #basicSetting[17] : 멍삭제횟수
	basicSetting.append(inputData[5][16:])     #basicSetting[18] : racing 채널 ID

	############## 보탐봇 명령어 리스트 #####################
	for i in range(len(command_inputData)):
		tmp_command = command_inputData[i][12:].rstrip('\r')
		fc = tmp_command.split(', ')
		command.append(fc)
		fc = []
		#command.append(command_inputData[i][12:].rstrip('\r'))     #command[0] ~ [24] : 명령어

	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()

	if basicSetting[6] != "":
		basicSetting[6] = int(basicSetting[6])

	if basicSetting[7] != "":
		basicSetting[7] = int(basicSetting[7])

	if basicSetting[8] != "":
		basicSetting[8] = int(basicSetting[8])

	if basicSetting[11] != "":
		basicSetting[11] = int(basicSetting[11])

	if basicSetting[18] != "":
		basicSetting[18] = int(basicSetting[18])

	tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

	if int(basicSetting[13]) == 0 :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		endTime = endTime + datetime.timedelta(days=int(1000))
	else :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		if endTime < tmp_now :
			endTime = endTime + datetime.timedelta(days=int(basicSetting[13]))

	### 채널 고정###
	#basicSetting[6] = int('597781866681991198') #보이스채널ID
	#basicSetting[7] = int('597782016607649829') #택스트채널ID

	bossNum = int(len(boss_inputData)/8)

	fixed_bossNum = int(len(fixed_inputData)/9)

	for i in range(bossNum):
		tmp_bossData.append(boss_inputData[i*8:i*8+8])

	for i in range(fixed_bossNum):
		tmp_fixed_bossData.append(fixed_inputData[i*9:i*9+9])

	#print (tmp_bossData)

	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()

	############## 일반보스 정보 리스트 #####################
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][3].find(':')
		f.append(tmp_bossData[j][0][11:])         #bossData[0] : 보스명
		f.append(tmp_bossData[j][3][10:tmp_len])  #bossData[1] : 시
		f.append(tmp_bossData[j][4][13:])         #bossData[2] : 멍/미입력
		f.append(tmp_bossData[j][5][20:])         #bossData[3] : 분전 알림멘트
		f.append(tmp_bossData[j][6][13:])         #bossData[4] : 젠 알림멘트
		f.append(tmp_bossData[j][3][tmp_len+1:])  #bossData[5] : 분
		f.append('')                              #bossData[6] : 메세지
		f.append(tmp_bossData[j][7][11:])         #bossData[7] : @everyone 알림
		f.append(tmp_bossData[j][1][15:])         #bossData[8] : 일본어 표기
		f.append(tmp_bossData[j][2][13:])         #bossData[9] : 한글 표기
		bossData.append(f)
		f = []
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('99:99:99')
		tmp_bossDateString.append('9999-99-99')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)
		bossMungTime.append('1987-09-12 10:30')
		bossAutoMungCnt.append(0)
		bossAutoMungTime.append('1987-09-12 10:30')

	tmp_fixed_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

	############## 고정보스 정보 리스트 #####################
	for j in range(fixed_bossNum):
		tmp_fixed_len = tmp_fixed_bossData[j][3].find(':')
		tmp_fixedGen_len = tmp_fixed_bossData[j][4].find(':')
		fb.append(tmp_fixed_bossData[j][0][11:])                  #fixed_bossData[0] : 보스명
		fb.append(tmp_fixed_bossData[j][3][11:tmp_fixed_len])     #fixed_bossData[1] : 시
		fb.append(tmp_fixed_bossData[j][3][tmp_fixed_len+1:])     #fixed_bossData[2] : 분
		fb.append(tmp_fixed_bossData[j][6][20:])                  #fixed_bossData[3] : 분전 알림멘트
		fb.append(tmp_fixed_bossData[j][7][13:])                  #fixed_bossData[4] : 젠 알림멘트
		fb.append(tmp_fixed_bossData[j][4][12:tmp_fixedGen_len])  #fixed_bossData[5] : 젠주기-시
		fb.append(tmp_fixed_bossData[j][4][tmp_fixedGen_len+1:])  #fixed_bossData[6] : 젠주기-분
		fb.append(tmp_fixed_bossData[j][5][12:16])                #fixed_bossData[7] : 시작일-년
		fb.append(tmp_fixed_bossData[j][5][17:19])                #fixed_bossData[8] : 시작일-월
		fb.append(tmp_fixed_bossData[j][5][20:22])                #fixed_bossData[9] : 시작일-일
		fb.append(tmp_fixed_bossData[j][8][11:])                  #fixed_bossData[10] : @everyone 알림
		fb.append(tmp_fixed_bossData[j][1][15:])                  #fixed_bossData[11] : 일본어 표기
		fb.append(tmp_fixed_bossData[j][2][13:])                  #fixed_bossData[12] : 한글 표기
		fixed_bossData.append(fb)
		fb = []
		fixed_bossFlag.append(False)
		fixed_bossFlag0.append(False)
		fixed_bossTime.append(tmp_fixed_now.replace(year = int(fixed_bossData[j][7]), month = int(fixed_bossData[j][8]), day = int(fixed_bossData[j][9]), hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
		if fixed_bossTime[j] < tmp_fixed_now :
			while fixed_bossTime[j] < tmp_fixed_now :
				fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(hours=int(fixed_bossData[j][5]), minutes=int(fixed_bossData[j][6]), seconds = int(0))

	################# 이모지 로드 ######################

	emo_inidata = repo.get_contents("emoji.ini")
	emoji_data1 = base64.b64decode(emo_inidata.content)
	emoji_data1 = emoji_data1.decode('utf-8')
	emo_inputData = emoji_data1.split('\n')

	for i in range(len(emo_inputData)):
		tmp_emo = emo_inputData[i][8:].rstrip('\r')
		if tmp_emo != "":
			tmp_racing_unit.append(tmp_emo)

	################# 리젠보스 시간 정렬 ######################
	regenData = []
	regenTime = []
	regenbossName = []
	outputTimeHour = []
	outputTimeMin = []

	for i in range(bossNum):
		f.append(bossData[i][0])
		f.append(bossData[i][1] + bossData[i][5])
		regenData.append(f)
		regenTime.append(bossData[i][1] + bossData[i][5])
		f = []

	regenTime = sorted(list(set(regenTime)))

	for j in range(len(regenTime)):
		for i in range(len(regenData)):
			if regenTime[j] == regenData[i][1] :
				f.append(regenData[i][0])
		regenbossName.append(f)
		outputTimeHour.append(int(regenTime[j][:2]))
		outputTimeMin.append(int(regenTime[j][2:]))
		f = []

	regenembed = discord.Embed(
			title='----- DBに登録されているボスリスト -----',
			description= ' ')
	for i in range(len(regenTime)):
		if outputTimeMin[i] == 0 :
			regenembed.add_field(name=str(outputTimeHour[i]) + '時間', value= '```'+ '、'.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
		else :
			regenembed.add_field(name=str(outputTimeHour[i]) + '時間' + str(outputTimeMin[i]) + '分', value= '```' + ','.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)

	##########################################################

	if basicSetting[10] !="":
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #정산
		credentials = ServiceAccountCredentials.from_json_keyfile_name(basicSetting[10], scope) #정산

init()

channel = ''

async def task():
	await client.wait_until_ready()

	global channel
	global endTime

	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt
	global bossMungTime
	global bossAutoMungCnt
	global bossAutoMungTime

	#voice:global voice_client1

	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type

	global endTime

	if chflg == 1 :
		#voice: if voice_client1.is_connected() == False :
		#voice: 	voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
		#voice: 	if voice_client1.is_connected() :
		await dbLoad()
		await client.get_channel(channel).send( '<戻りました！>', tts=False)
		print("명치복구완료!")

	while not client.is_closed():
		############ 워닝잡자! ############
		if log_stream.getvalue().find("Awaiting") != -1:
			log_stream.truncate(0)
			log_stream.seek(0)
			await client.get_channel(channel).send( '<接続エラーが発生しました。直らない場合、管理者までご連絡ください！>', tts=False)
			await dbSave()
			raise SystemExit

		log_stream.truncate(0)
		log_stream.seek(0)
		##################################

		now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))

		if channel != '':
			################ 보탐봇 재시작 ################
			if endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M:%S'):
				await dbSave()
				await FixedBossDateSave()
				await client.get_channel(channel).send('<再起動します。>', tts=False)
				print("보탐봇재시작!")
				endTime = endTime + datetime.timedelta(days = int(basicSetting[13]))
				#voice:await voice_client1.disconnect()
				await asyncio.sleep(2)

				inidata_restart = repo_restart.get_contents("restart.txt")
				file_data_restart = base64.b64decode(inidata_restart.content)
				file_data_restart = file_data_restart.decode('utf-8')
				inputData_restart = file_data_restart.split('\n')

				if len(inputData_restart) < 3:
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
				else:
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)

			################ 고정 보스 확인 ################
			for i in range(fixed_bossNum):
				################ before_alert1 ################
				if fixed_bossTime[i] <= priv0 and fixed_bossTime[i] > priv:
					if basicSetting[3] != '0':
						if fixed_bossFlag0[i] == False:
							fixed_bossFlag0[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][11] + ' ' + basicSetting[3] + 'minutes' + fixed_bossData[i][3] +'[' +  fixed_bossTime[i].strftime('%H:%M') + ']```', tts=False)
							#voice:await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림1.mp3')

				################ before_alert ################
				if fixed_bossTime[i] <= priv and fixed_bossTime[i] > now:
					if basicSetting[1] != '0' :
						if fixed_bossFlag[i] == False:
							fixed_bossFlag[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][11] + ' ' + basicSetting[1] + 'minutes' + fixed_bossData[i][3] +'[' +  fixed_bossTime[i].strftime('%H:%M') + ']```', tts=False)
							# @everyone 전체공지
							if int(fixed_bossData[i][10]) == 1 :
								await client.get_channel(channel).send("@everyone " + fixed_bossData[i][11] + ' ' + basicSetting[1] + 'minutes !', tts=False)
							#voice:await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림.mp3')

				################ 보스 젠 시간 확인 ################
				if fixed_bossTime[i] <= now :
					fixed_bossTime[i] = fixed_bossTime[i]+datetime.timedelta(hours=int(fixed_bossData[i][5]), minutes=int(fixed_bossData[i][6]), seconds = int(0))
					fixed_bossFlag0[i] = False
					fixed_bossFlag[i] = False
					embed = discord.Embed(
							description= "```" + fixed_bossData[i][11] + '' + fixed_bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send(embed=embed, tts=False)
					# @everyone 전체공지
					if int(fixed_bossData[i][10]) == 1 :
						await client.get_channel(channel).send("@everyone " + fixed_bossData[i][11] + ' Time！', tts=False)
					#voice:await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '젠.mp3')

			################ 일반 보스 확인 ################
			for i in range(bossNum):
				################ before_alert1 ################
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							# 자동 멍처리가 있었던 경우 미확인 표시
							prefixStirng = ''
							if bossAutoMungCnt[i] > 0 :
								prefixStirng = '[未] '
							# 보스 메모 유무
							if bossData[i][6] != '' :
								await client.get_channel(channel).send("```" + prefixStirng + bossData[i][8] + ' ' + basicSetting[3] + 'minutes' + bossData[i][3] + "[" +  bossTimeString[i] + "]" + '\n<' + bossData[i][6] + '>```', tts=False)
							else :
								await client.get_channel(channel).send("```" + prefixStirng + bossData[i][8] + ' ' + basicSetting[3] + 'minutes' + bossData[i][3] + "[" +  bossTimeString[i] + "]```", tts=False)
							#voice:await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')

				################ before_alert ################
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							# 자동 멍처리가 있었던 경우 미확인 표시
							prefixStirng = ''
							if bossAutoMungCnt[i] > 0 :
								prefixStirng = '[未] '
							# 보스 메모 유무
							if bossData[i][6] != '' :
								await client.get_channel(channel).send("```" + prefixStirng + bossData[i][8] + ' ' + basicSetting[1] + 'minutes' + bossData[i][3] + "[" +  bossTimeString[i] + "]" + '\n<' + bossData[i][6] + '>```', tts=False)
							else :
								await client.get_channel(channel).send("```" + prefixStirng + bossData[i][8] + ' ' + basicSetting[1] + 'minutes' + bossData[i][3] + "[" +  bossTimeString[i] + "]```", tts=False)
							# @everyone 전체공지
							if int(bossData[i][7]) == 1 :
								await client.get_channel(channel).send("@everyone " + prefixStirng + bossData[i][8] + ' ' + basicSetting[1] + 'minutes !', tts=False)
							#voice:await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')

				################ 보스 젠 시간 확인 ################
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					tmp_bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
					tmp_bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					# 자동 멍처리가 있었던 경우 미확인 표시
					prefixStirng = ''
					if bossAutoMungCnt[i] > 0 :
						prefixStirng = '[未] '
					bossTime[i] = now+datetime.timedelta(days=365)
					# 보스 메모 유무
					if bossData[i][6] != '' :
						embed = discord.Embed(
								description= '```' + prefixStirng + bossData[i][8] + '' + bossData[i][4] + '\n<' + bossData[i][6] + '>```' ,
								color=0x00ff00
								)
					else :
						embed = discord.Embed(
								description= '```' + prefixStirng + bossData[i][8] + '' + bossData[i][4] + '```',
								color=0x00ff00
								)
					await client.get_channel(channel).send(embed=embed, tts=False)
					# @everyone 전체공지
					if int(bossData[i][7]) == 1 :
						await client.get_channel(channel).send("@everyone " + prefixStirng + bossData[i][8] + " Time！", tts=False)
					#voice:await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')

				################ 보스 자동 멍 처리 ################
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						if basicSetting[2] != '0':
							if int(basicSetting[17]) <= bossAutoMungCnt[i] and int(basicSetting[17]) != 0:
								bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
								tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
								bossTimeString[i] = '99:99:99'
								bossDateString[i] = '9999-99-99'
								tmp_bossTimeString[i] = '99:99:99'
								tmp_bossDateString[i] = '9999-99-99'
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								#bossMungCnt[i] = 0
								bossAutoMungCnt[i] = 0
								await client.get_channel(channel).send('```' + bossData[i][0] + 'の未記入処理回数が' + basicSetting[17] + '回を超えました。\n管理されていないボスとして時間記録を削除します。```', tts=False)
								print ('자동미입력 횟수초과 <' + bossData[i][0] + '> 삭제완료')
								#await dbSave()

							else:
								################ 미입력 보스 ################
								if bossData[i][2] == '0':
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									#bossMungCnt[i] = bossMungCnt[i] + 1
									bossAutoMungCnt[i] = bossAutoMungCnt[i] + 1
									tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									await client.get_channel(channel).send("```" +  bossData[i][0] + 'のエンド時間が入力されませんでした。未記入処理します。```', tts=False)
									embed = discord.Embed(
										description= '```次、' + bossData[i][0] + 'の湧き予想時間は ' + bossTimeString[i] + ' です。```',
										color=0xff0000
										)
									await client.get_channel(channel).send(embed=embed, tts=False)
									#voice:await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
								################ 멍 보스 ################
								else :
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									#bossMungCnt[i] = bossMungCnt[i] + 1
									bossAutoMungCnt[i] = bossAutoMungCnt[i] + 1
									tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									await client.get_channel(channel).send("```" + bossData[i][0] + 'の「cut」、または「pass」が入力されませんでした。未記入処理します。```')
									embed = discord.Embed(
										description= '```次、' + bossData[i][0] + 'の湧き予想時間は ' + bossTimeString[i] + ' です。```',
										color=0xff0000
										)
									await client.get_channel(channel).send(embed=embed, tts=False)
									#voice:await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')

		await asyncio.sleep(1) # task runs every 60 seconds

#mp3 파일 생성함수(gTTS 이용, 남성목소리)
async def MakeSound(saveSTR, filename):

	tts = gTTS(saveSTR, lang = 'jp')
	tts.save('./' + filename + '.wav')

	'''
	try:
		encText = urllib.parse.quote(saveSTR)
		urllib.request.urlretrieve("https://clova.ai/proxy/voice/api/tts?text=" + encText + "%0A&voicefont=1&format=wav",filename + '.wav')
	except Exception as e:
		print (e)
		tts = gTTS(saveSTR, lang = 'jp')
		tts.save('./' + filename + '.wav')
		pass
	'''
#mp3 파일 재생함수
async def PlaySound(voiceclient, filename):
	source = discord.FFmpegPCMAudio(filename)
	try:
		voiceclient.play(source)
	except discord.errors.ClientException:
		while voiceclient.is_playing():
			await asyncio.sleep(1)
	while voiceclient.is_playing():
		await asyncio.sleep(1)
	voiceclient.stop()
	source.cleanup()

#my_bot.db 저장하기
async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungFlag
	global bossMungCnt
	global bossMungTime
	global bossAutoMungCnt
	global bossAutoMungTime

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22

	datelist1 = bossTime

	datelist = list(set(datelist1))

	information1 = '----- ボス湧き情報 -----\n'
	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' or bossMungFlag[i] == True :
					if bossMungFlag[i] == True :
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (미 ' + str(bossAutoMungCnt[i]) + '회 # ' + bossAutoMungTime[i] + ')' + ' * ' + bossData[i][6] + '\n'
						else :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (멍 ' +  str(bossMungCnt[i]) + '회 $ ' + bossMungTime[i] + ' & 미 ' + str(bossAutoMungCnt[i]) + '회 # ' + bossAutoMungTime[i] + ')' + ' * ' + bossData[i][6] + '\n'
					else:
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미 ' + str(bossAutoMungCnt[i]) + '회 # ' + bossAutoMungTime[i] + ')' + ' * ' + bossData[i][6] + '\n'
						else :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' +  str(bossMungCnt[i]) + '회 $ ' + bossMungTime[i] + ' & 미 ' + str(bossAutoMungCnt[i]) + '회 # ' + bossAutoMungTime[i] + ')' + ' * ' + bossData[i][6] + '\n'

	try :
		contents = repo.get_contents("my_bot.db")
		repo.update_file(contents.path, "bossDB", information1, contents.sha)
	except GithubException as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#my_bot.db 불러오기
async def dbLoad():
	global LoadChk

	contents1 = repo.get_contents("my_bot.db")
	file_data = base64.b64decode(contents1.content)
	file_data = file_data.decode('utf-8')
	beforeBossData = file_data.split('\n')

	if len(beforeBossData) > 1:
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				startPos = beforeBossData[i+1].find('-')
				endPos = beforeBossData[i+1].find('(')
				if beforeBossData[i+1][startPos+2:endPos] == bossData[j][0] :
				#if beforeBossData[i+1].find(bossData[j][0]) != -1 :
					tmp_mungcnt = 0
					tmp_automungcnt = 0
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')
					tmp_munglen = beforeBossData[i+1].find('$')
					tmp_automunglen = beforeBossData[i+1].find('#')
					tmp_msglen = beforeBossData[i+1].find('*')

					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]

					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]

					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

					tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					tmp_now_chk = tmp_now + datetime.timedelta(minutes = int(basicSetting[2]))

					if tmp_now_chk < now2 :
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while tmp_now_chk < now2 :
							tmp_now_chk = tmp_now_chk + deltaTime
							tmp_now = tmp_now + deltaTime
							#tmp_mungcnt = tmp_mungcnt + 1
							tmp_automungcnt = tmp_automungcnt + 1

					if tmp_now_chk > now2 > tmp_now: #젠중.
						bossMungFlag[j] = True
						tmp_bossTime[j] = tmp_now
						tmp_bossTimeString[j] = tmp_bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = tmp_bossTime[j].strftime('%Y-%m-%d')
						bossTimeString[j] = '99:99:99'
						bossDateString[j] = '9999-99-99'
						bossTime[j] = tmp_bossTime[j] + datetime.timedelta(days=365)
					else:
						tmp_bossTime[j] = bossTime[j] = tmp_now
						tmp_bossTimeString[j] = bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')

					bossData[j][6] = beforeBossData[i+1][tmp_msglen+2:len(beforeBossData[i+1])]
					bossMungTime[j] = beforeBossData[i+1][tmp_munglen+2:tmp_munglen+18]
					bossAutoMungTime[j] = beforeBossData[i+1][tmp_automunglen+2:tmp_automunglen+18]

					if tmp_munglen != -1 :
						if beforeBossData[i+1][tmp_munglen-3:tmp_munglen-2] != 0 and beforeBossData[i+1][tmp_munglen-4:tmp_munglen-3] == ' ':
							bossMungCnt[j] = int(beforeBossData[i+1][tmp_munglen-3:tmp_munglen-2]) + tmp_mungcnt
						elif beforeBossData[i+1][tmp_munglen-4:tmp_munglen-3] != ' ':
							bossMungCnt[j] = int(beforeBossData[i+1][tmp_munglen-4:tmp_munglen-3] + beforeBossData[i+1][tmp_munglen-3:tmp_munglen-2]) + tmp_mungcnt
						else:
							bossMungCnt[j] = 0

					if beforeBossData[i+1][tmp_automunglen-3:tmp_automunglen-2] != 0 and beforeBossData[i+1][tmp_automunglen-4:tmp_automunglen-3] == ' ':
						bossAutoMungCnt[j] = int(beforeBossData[i+1][tmp_automunglen-3:tmp_automunglen-2]) + tmp_automungcnt
					elif beforeBossData[i+1][tmp_automunglen-4:tmp_automunglen-3] != ' ':
						bossAutoMungCnt[j] = int(beforeBossData[i+1][tmp_automunglen-4:tmp_automunglen-3] + beforeBossData[i+1][tmp_automunglen-3:tmp_automunglen-2]) + tmp_automungcnt
					else:
						bossAutoMungCnt[j] = 0
		LoadChk = 0
		print ("<불러오기 완료>")
	else:
		#await client.get_channel(channel).send('<보스타임 정보가 없습니다.>', tts=False)
		LoadChk = 1
		print ("보스타임 정보가 없습니다.")

#고정보스 날짜저장
async def FixedBossDateSave():
	global fixed_bossData
	global fixed_bossTime
	global fixed_bossNum
	global FixedBossDateData
	global indexFixedBossname

	for i in range(fixed_bossNum):
		FixedBossDateData[indexFixedBossname[i] + 5] = 'startDate = '+ fixed_bossTime[i].strftime('%Y-%m-%d') + '\n'

	FixedBossDateDataSTR = ""
	for j in range(len(FixedBossDateData)):
		pos = len(FixedBossDateData[j])
		tmpSTR = FixedBossDateData[j][:pos-1] + '\r\n'
		FixedBossDateDataSTR += tmpSTR

	contents = repo.get_contents("fixed_boss.ini")
	repo.update_file(contents.path, "bossDB", FixedBossDateDataSTR, contents.sha)

#사다리함수
async def LadderFunc(number, ladderlist, channelVal):
	if number < len(ladderlist):
		result_ladder = random.sample(ladderlist, number)
		result_ladderSTR = '、'.join(map(str, result_ladder))
		embed = discord.Embed(
			title = "----- 当たり！ -----",
			description= '```' + result_ladderSTR + '```',
			color=0xff00ff
			)
		await channelVal.send(embed=embed, tts=False)
	else:
		await channelVal.send('```抽選人数が参加人数と同じか、多いです。設定し直してください。```', tts=False)

#초성추출 함수
def convertToInitialLetters(text):
	CHOSUNG_START_LETTER = 4352
	JAMO_START_LETTER = 44032
	JAMO_END_LETTER = 55203
	JAMO_CYCLE = 588

	def isHangul(ch):
		return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER

	def isBlankOrNumber(ch):
		return ord(ch) == 32 or ord(ch) >= 48 and ord(ch) <= 57

	def convertNomalInitialLetter(ch):
		dic_InitalLetter = {4352:"ㄱ"
							,4353:"ㄲ"
							,4354:"ㄴ"
							,4355:"ㄷ"
							,4356:"ㄸ"
							,4357:"ㄹ"
							,4358:"ㅁ"
							,4359:"ㅂ"
							,4360:"ㅃ"
							,4361:"ㅅ"
							,4362:"ㅆ"
							,4363:"ㅇ"
							,4364:"ㅈ"
							,4365:"ㅉ"
							,4366:"ㅊ"
							,4367:"ㅋ"
							,4368:"ㅌ"
							,4369:"ㅍ"
							,4370:"ㅎ"
							,32:" "
							,48:"0"
							,49:"1"
							,50:"2"
							,51:"3"
							,52:"4"
							,53:"5"
							,54:"6"
							,55:"7"
							,56:"8"
							,57:"9"
		}
		return dic_InitalLetter[ord(ch)]

	result = ""
	for ch in text:
		if isHangul(ch): #한글이 아닌 글자는 걸러냅니다.
			result += convertNomalInitialLetter(chr((int((ord(ch)-JAMO_START_LETTER)/JAMO_CYCLE))+CHOSUNG_START_LETTER))
		elif isBlankOrNumber(ch):
			result += convertNomalInitialLetter(chr(int(ord(ch))))

	return result

## 명치 예외처리
def handle_exit():
	#print("Handling")
	client.loop.run_until_complete(client.logout())

	for t in asyncio.Task.all_tasks(loop=client.loop):
		if t.done():
		#t.exception()
			try:
			#print ('try :   ', t)
				t.exception()
			except asyncio.CancelledError:
			#print ('cancel :   ', t)
				continue
			continue
		t.cancel()
		try:
			client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
			t.exception()
		except asyncio.InvalidStateError:
			pass
		except asyncio.TimeoutError:
			pass
		except asyncio.CancelledError:
			pass

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
	global channel

	#voice:global voice_client1

	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type

	global chkvoicechannel
	global chflg

	global endTime

	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")


	#await joinVoiceChannel()
	all_channels = client.get_all_channels()

	for channel1 in all_channels:
		channel_type.append(str(channel1.type))
		channel_info.append(channel1)

	for i in range(len(channel_info)):
		if channel_type[i] == "text":
			channel_name.append(str(channel_info[i].name))
			channel_id.append(str(channel_info[i].id))

	for i in range(len(channel_info)):
		if channel_type[i] == "voice":
			channel_voice_name.append(str(channel_info[i].name))
			channel_voice_id.append(str(channel_info[i].id))

	await dbLoad()

	if basicSetting[7] != "" :
		#print ('join channel')
		#voice:voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
		channel = basicSetting[7]

		print('<텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>')
		if basicSetting[6] != "":
			print('<음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>')
		if basicSetting[8] != "":
			print('<사다리채널 [' + client.get_channel(int(basicSetting[8])).name + '] 접속완료>')
		if basicSetting[11] != "":
			print('<정산채널 [' + client.get_channel(int(basicSetting[11])).name + '] 접속완료>')
		if basicSetting[18] != "":
			print('<경주채널 [' + client.get_channel(int(basicSetting[18])).name + '] 접속완료>')
		if int(basicSetting[13]) != 0 :
			print('<보탐봇 재시작 시간 ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + '>')
			print('<보탐봇 재시작 주기 ' + basicSetting[13] + '일>')
		else :
			print('<보탐봇 재시작 설정안됨>')
		chflg = 1

	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=command[1][0], type=1), afk=False)

while True:
	################ 보탐봇 입장 ################
	@client.command(name=command[0][0], aliases=command[0][1:])
	async def join_(ctx):
		global basicSetting
		global chflg
		#voice:global voice_client1

		if basicSetting[7] == "":
			channel = ctx.message.channel.id #메세지가 들어온 채널 ID

			print ('[ ', basicSetting[7], ' ]')
			print ('] ', ctx.message.channel.name, ' [')

			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')

			for i in range(len(inputData_textCH)):
				if inputData_textCH[i] == 'textchannel = \r':
					inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
					basicSetting[7] = channel
					#print ('======', inputData_text[i])

			result_textCH = '\n'.join(inputData_textCH)

			#print (result_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			#voice:await ctx.send('<텍스트채널 [' + ctx.message.channel.name + '] 접속완료>\n<음성채널 접속 후 [소환] 명령을 사용 하세요>', tts=False)

			print('<텍스트채널 [' + client.get_channel(channel).name + '] 접속완료>')

			if basicSetting[6] != "":
				#voice:voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
				print('<음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>')
			if basicSetting[8] != "":
				print('<사다리채널 [' + client.get_channel(int(basicSetting[8])).name + '] 접속완료>')
			if basicSetting[11] != "":
				print('<정산채널 [' + client.get_channel(int(basicSetting[11])).name + '] 접속완료>')
			if basicSetting[18] != "":
				print('<경주채널 [' + client.get_channel(int(basicSetting[18])).name + '] 접속완료>')
			if int(basicSetting[13]) != 0 :
				print('<보탐봇 재시작 시간 ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + '>')
				print('<보탐봇 재시작 주기 ' + basicSetting[13] + '일 >')
			else :
				print('<보탐봇 재시작 설정안됨 >')

			chflg = 1
		else:
			await ctx.send('すでに [' + ctx.guild.get_channel(basicSetting[7]).name + '] チャンネルに接続しています。該当チャンネルでコマンドを入力してください！\n', tts=False)

	################ 보탐봇 메뉴 출력 ################
	@client.command(name=command[1][0], aliases=command[1][1:])
	async def menu_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			command_list = ''
			command_list += '<1.ボスの情報確認>\n\n'
			command_list += '、'.join(command[22]) + '\n -> 全体ボス湧き情報の一覧を表示します。\n\n'                      #보스탐
			command_list += '、'.join(command[17]) + '\n -> DBに登録されている各ボスの名称と湧き時間を表示します。\n\n'         #!리젠
			command_list += '\n<2.ボスの情報記録>\n\n'
			command_list += '[ボス名]エンド または [ボス名]エンド0000\n -> 例えば、「Gドレエンド」と入力すると自動でエンド時間を記録します。\n -> 「Gドレエンド1530」のように指定時間の入力も可能です。\n\n'
			command_list += '[ボス名]なし または [ボス名]なし0000\n -> ボスが湧かなかった場合、記録しておくための機能です。\n\n'
			command_list += '[ボス名]予想0000\n -> 次のボス湧き予想時間を登録できます。\n\n'
			command_list += '[ボス名]　(スペース)[メモ内容]\n[ボス名]：(コロン)[メモ内容]\n -> 該当ボスに何か情報をメモしたい場合使います。\n\n'
			command_list += '[ボス名]メモ削除\n -> ボスに登録したメモを削除します。\n\n'
			command_list += '[ボス名]削除\n -> ボスのエンド時間記録を削除します。\n\n'
			command_list += '、'.join(command[7]) + '\n -> 登録されているボスエンド記録を全てDBから削除します。（復元可能）\n * メンテナンス後におすすめ。\n\n'       #!초기화
			command_list += '\n<便利機能>\n\n'
			command_list += '、'.join(command[18]) + '\n -> 現在時刻\n\n'     #!현재시간
			command_list += '、'.join(command[11]) + '　(スペース)[人数]：(コロン)[金額]\n -> 実質分配金額を計算します。(税率５％基準)\n\n'                             #!분배
			command_list += '、'.join(command[12]) + '　(スペース)[抽選人数]：(コロン)[名前１]：(コロン)[名前２]...\n -> 競売ではなく抽選で決める際活用してください。\n\n'     #!사다리
			command_list += '、'.join(command[24]) + '　(スペース)[名前１]：(コロン)[名前２]：(コロン)[名前３]...\n -> ワクワクレーシング！(最大１２名まで）\n\n'            #!경주
			command_list += '\n<何かおかしくなったら?>\n\n'
			command_list += '、'.join(command[8]) + '\n -> データを全て正しく整理し、DBに入れ直します。\n\n'      #!명치
			command_list += '、'.join(command[9]) + '\n -> ボットを再起動します。\n\n'                      #!재시작
			command_list += '\n<設定>\n\n'
			command_list += '、'.join(command[2]) + '\n -> 設定を確認します。\n\n'     #!설정확인
			command_list += '、'.join(command[3]) + '\n -> 移動可能なテキストチャンネルのリストを表示します。\n\n'              #!채널확인
			command_list += '、'.join(command[4]) + '　(スペース)[チャンネル名]\n -> 指定したチャンネルに移動します。\n\n'               #!채널이동
			# command_list += '\n<未使用機能>\n'
			# command_list += command[21] + '\n -> 固定時間ボスを分け、全体ボス湧き情報の一覧を表示します。\n\n'        #!보스탐
			# command_list += command[14] + ' または ！つぎ\n -> もうすぐで沸くボスのリストを簡略に表示します。\n\n'     #!q
			# command_list += command[9] + '\n -> 確認されていないボスを表示します。\n\n'                         #!미예약
			# command_list += command[4] + '\n -> 召喚したユーザーのいるボイスチャンネルにボットが召喚されます。\n\n'     #!소환
			# command_list += command[19] + '：[内容]\n -> ボットの状態メッセージを変更します。\n\n'     #!상태
			# command_list += command[18] + '\n -> 登録されているお知らせを確認できます。\n\n'     #!공지
			# command_list += command[18] + '：[お知らせ内容]\n -> お知らせを登録できます。\n\n'   #!공지
			# command_list += command[18] + '削除\n -> 登録されているお知らせを削除します。\n\n'    #!공지
			# command_list += command[5] + '\n -> <使用禁止> ボット管理者用の機能です。\n\n'     #!불러오기
			# command_list += command[13] + ' または ' + command[13] + '0000\n -> ボス全体の時間を一括で入力します。\n\n'     #!보스일괄
			# command_list += command[12] + '：[名前]\n -> <アップデート予定> 血盟の予算管理用の機能です。\n\n'     #!정산
			# command_list += command[15] + '：[内容]\n -> <アップデート予定> TTS(テキストをボットが読み上げる)機能です。\n\n'     #!v
			# command_list += command[22] + '\n -> キル記録を初期化します。\n\n'   #!킬초기화
			# command_list += command[23] + '\n -> キル回数を確認します。\n\n'     #!킬횟수 확인
			# command_list += command[23] + '：[名前]\n\n'                     #!킬
			# command_list += command[24] + '：[名前]\n\n'                     #!킬삭제
			command_list += '\n'
			embed = discord.Embed(
					title = "----- 説明書 -----",
					description= '```' + command_list + '```',
					color=0xff00ff
					)
			embed.add_field(
					name="----- 注意 -----",
					value= '```分単位でボスを管理しているため、最大59秒まで湧き時間に誤差があります。```'
					#value= '```日本語の場合は「！」を、英語の場合は「!」を使い分けてください。\n(ex.！説明書、!v)```'
					)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 보탐봇 기본 설정확인 ################
	@client.command(name=command[2][0], aliases=command[2][1:])
	async def setting_(ctx):
		#print (ctx.message.channel.id)
		if ctx.message.channel.id == basicSetting[7]:
			setting_val = 'Version : 16.60 (2020-06-07)\n'
			setting_val += 'テキストチャンネル : ' + client.get_channel(basicSetting[7]).name + '\n'
			if basicSetting[6] != "" :
				setting_val += 'ボイスチャンネル : ' + client.get_channel(basicSetting[6]).name + '\n'
			if basicSetting[8] != "" :
				setting_val += '抽選チャンネル : ' + client.get_channel(int(basicSetting[8])).name + '\n'
			if basicSetting[11] != "" :
				setting_val += '精算チャンネル : ' + client.get_channel(int(basicSetting[11])).name + '\n'
			if basicSetting[18] != "" :
				setting_val += 'レーシングチャンネル : ' + client.get_channel(int(basicSetting[18])).name + '\n'
			setting_val += 'ボス湧きアラート1 : ' + basicSetting[1] + '分前\n'
			setting_val += 'ボス湧きアラート2 : ' + basicSetting[3] + '分前\n'
			setting_val += 'ボス湧き時間のアラートから未記入処理までの入力待機時間 : ' + basicSetting[2] + '分\n'
			setting_val += '最大未記入回数 : ' + basicSetting[17] + '回\n'
			embed = discord.Embed(
					title = "----- 設定内容 -----",
					description= '```' + setting_val + '```',
					color=0xff00ff
					)
			await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 서버 채널 확인 ################
	@client.command(name=command[3][0], aliases=command[3][1:])
	async def chChk_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			ch_information = []
			cnt = 0
			ch_information.append('')
			for i in range(len(channel_name)):
				if len(ch_information[cnt]) > 900 :
					ch_information.append('')
					cnt += 1
				ch_information[cnt] = ch_information[cnt] + '[' + channel_id[i] + '] ' + channel_name[i] + '\n'

			ch_voice_information = []
			cntV = 0
			ch_voice_information.append('')
			for i in range(len(channel_voice_name)):
				if len(ch_voice_information[cntV]) > 900 :
					ch_voice_information.append('')
					cntV += 1
				ch_voice_information[cntV] = ch_voice_information[cntV] + '[' + channel_voice_id[i] + '] ' + channel_voice_name[i] + '\n'

			if len(ch_information) == 1 and len(ch_voice_information) == 1:
				embed = discord.Embed(
					title = "----- チャンネル情報 -----",
					description= '',
					color=0xff00ff
					)
				embed.add_field(
					name="<テキストチャンネル>",
					value= '```' + ch_information[0] + '```',
					inline = False
					)
				embed.add_field(
					name="<ボイスチャンネル>",
					value= '```' + ch_voice_information[0] + '```',
					inline = False
					)

				await ctx.send(embed=embed, tts=False)
			else :
				embed = discord.Embed(
					title = "----- チャンネル情報 -----\n<テキストチャンネル>",
					description= '```' + ch_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send(embed=embed, tts=False)
				for i in range(len(ch_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send(embed=embed, tts=False)
				embed = discord.Embed(
					title = "<ボイスチャンネル>",
					description= '```' + ch_voice_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send(embed=embed, tts=False)
				for i in range(len(ch_voice_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_voice_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 텍스트채널이동 ################
	@client.command(name=command[4][0], aliases=command[4][1:])
	async def chMove_(ctx):
		global basicSetting
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(len(channel_name)):
				if  channel_name[i] == msg:
					channel = int(channel_id[i])

			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')

			for i in range(len(inputData_textCH)):
				if inputData_textCH[i] == 'textchannel = ' + str(basicSetting[7]) + '\r':
					inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
					basicSetting[7] = int(channel)

			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			await ctx.send( f'チャンネル移動 <{ctx.message.channel.name}> -> <{client.get_channel(channel).name}>', tts=False)
			await client.get_channel(channel).send( f'<{client.get_channel(channel).name}>チャンネル到着', tts=False)
		else:
			return

	################ 보탐봇 음성채널 소환 ################
	# @client.command(name=command[5][0], aliases=command[5][1:])
	# async def connectVoice_(ctx):
	# 	global voice_client1
	# 	global basicSetting
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		if ctx.voice_client is None:
	# 			if ctx.author.voice:
	# 				voice_client1 = await ctx.author.voice.channel.connect(reconnect = True)
	# 			else:
	# 				await ctx.send('음성채널에 먼저 들어가주세요.', tts=False)
	# 				return
	# 		else:
	# 			if ctx.voice_client.is_playing():
	# 				ctx.voice_client.stop()

	# 			await ctx.voice_client.move_to(ctx.author.voice.channel)

	# 		voice_channel = ctx.author.voice.channel

	# 		print ('< ', basicSetting[6], ' >')
	# 		print ('> ', client.get_channel(voice_channel.id).name, ' <')

	# 		if basicSetting[6] == "":
	# 			inidata_voiceCH = repo.get_contents("test_setting.ini")
	# 			file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
	# 			file_data_voiceCH = file_data_voiceCH.decode('utf-8')
	# 			inputData_voiceCH = file_data_voiceCH.split('\n')

	# 			for i in range(len(inputData_voiceCH)):
	# 				if inputData_voiceCH[i] == 'voicechannel = \r':
	# 					inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
	# 					basicSetting[6] = int(voice_channel.id)

	# 			result_voiceCH = '\n'.join(inputData_voiceCH)

	# 			contents = repo.get_contents("test_setting.ini")
	# 			repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

	# 		elif basicSetting[6] != int(voice_channel.id):
	# 			inidata_voiceCH = repo.get_contents("test_setting.ini")
	# 			file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
	# 			file_data_voiceCH = file_data_voiceCH.decode('utf-8')
	# 			inputData_voiceCH = file_data_voiceCH.split('\n')

	# 			for i in range(len(inputData_voiceCH)):
	# 				if inputData_voiceCH[i] == 'voicechannel = ' + str(basicSetting[6]) + '\r':
	# 					inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
	# 					basicSetting[6] = int(voice_channel.id)

	# 			result_voiceCH = '\n'.join(inputData_voiceCH)

	# 			contents = repo.get_contents("test_setting.ini")
	# 			repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

	# 		await ctx.send('<음성채널 [' + client.get_channel(voice_channel.id).name + '] 접속완료>', tts=False)
	# 	else:
	# 		return


	################ my_bot.db에 저장된 보스타임 불러오기 ################
	@client.command(name=command[6][0], aliases=command[6][1:])
	async def loadDB_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await dbLoad()

			if LoadChk == 0:
				await ctx.send('<DBを読み込みました。>', tts=False)
			else:
				await ctx.send('<データがありません。>', tts=False)
		else:
			return

	################ 저장된 정보 초기화 ################
	@client.command(name=command[7][0], aliases=command[7][1:])
	async def initVal_(ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime
		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global fixed_bossFlag
		global fixed_bossFlag0
		global bossMungFlag
		global bossMungCnt
		global bossMungTime
		global bossAutoMungCnt
		global bossAutoMungTime

		global FixedBossDateData
		global indexFixedBossname

		if ctx.message.channel.id == basicSetting[7]:
			basicSetting = []
			bossData = []
			fixed_bossData = []

			bossTime = []
			tmp_bossTime = []
			fixed_bossTime = []

			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []

			bossFlag = []
			bossFlag0 = []
			fixed_bossFlag = []
			fixed_bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []
			bossMungTime = []
			bossAutoMungCnt = []
			bossAutoMungTime = []

			FixedBossDateData = []
			indexFixedBossname = []

			init()

			await dbSave()

			await ctx.send('<データを初期化しました。>', tts=False)
			print ("<초기화 완료>")
		else:
			return


	################ 명존쎄 ################
	@client.command(name=command[8][0], aliases=command[8][1:])
	async def mungchi_(ctx):
		global basicSetting
		global bossTimeString
		global bossDateString
		global bossFlag
		global bossFlag0
		global bossMungFlag

		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send( '<データをDBに入れ直します。>', tts=False)
			await dbSave()
			print("명치!")
			#voice:await voice_client1.disconnect()
			#client.clear()
			raise SystemExit
		else:
			return

	################ 보탐봇 재시작 ################
	@client.command(name=command[9][0], aliases=command[9][1:])
	async def restart_(ctx):
		global basicSetting
		global bossTimeString
		global bossDateString

		if ctx.message.channel.id == basicSetting[7]:
			if basicSetting[2] != '0':
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
			await dbSave()
			#voice:await voice_client1.disconnect()
			#await FixedBossDateSave()
			#await client.get_channel(channel).send('<보탐봇 재시작 중... 갑자기 인사해도 놀라지마세요!>', tts=False)
			await ctx.send('システムを再起動します。<所要時間：約５分>', tts=False)
			print("보탐봇강제재시작!")
			await asyncio.sleep(2)

			inidata_restart = repo_restart.get_contents("restart.txt")
			file_data_restart = base64.b64decode(inidata_restart.content)
			file_data_restart = file_data_restart.decode('utf-8')
			inputData_restart = file_data_restart.split('\n')

			if len(inputData_restart) < 3:
				contents12 = repo_restart.get_contents("restart.txt")
				repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
			else:
				contents12 = repo_restart.get_contents("restart.txt")
				repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)
		else:
			return

	################ 미예약 보스타임 출력 ################ 
	# @client.command(name=command[10][0], aliases=command[10][1:])
	# async def nocheckBoss_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		tmp_boss_information = []
	# 		tmp_cnt = 0
	# 		tmp_boss_information.append('')

	# 		for i in range(bossNum):
	# 			if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
	# 				if len(tmp_boss_information[tmp_cnt]) > 1800 :
	# 					tmp_boss_information.append('')
	# 					tmp_cnt += 1
	# 				tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','

	# 		if len(tmp_boss_information) == 1:
	# 			if len(tmp_boss_information[0]) != 0:
	# 				tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
	# 			else :
	# 				tmp_boss_information[0] = '``` ```'

	# 			embed = discord.Embed(
	# 					title = "----- 미예약 보스 -----",
	# 					description= tmp_boss_information[0],
	# 					color=0x0000ff
	# 					)
	# 			await ctx.send( embed=embed, tts=False)
	# 		else:
	# 			if len(tmp_boss_information[0]) != 0:
	# 				if len(tmp_boss_information) == 1 :
	# 					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
	# 				else:
	# 					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
	# 			else :
	# 				tmp_boss_information[0] = '``` ```'

	# 			embed = discord.Embed(
	# 				title = "----- 미예약 보스 -----",
	# 				description= tmp_boss_information[0],
	# 				color=0x0000ff
	# 				)
	# 			await ctx.send( embed=embed, tts=False)
	# 			for i in range(len(tmp_boss_information)-1):
	# 				if len(tmp_boss_information[i+1]) != 0:
	# 					if i == len(tmp_boss_information)-2:
	# 						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
	# 					else:
	# 						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"							
	# 				else :
	# 					tmp_boss_information[i+1] = '``` ```'

	# 				embed = discord.Embed(
	# 						title = '',
	# 						description= tmp_boss_information[i+1],
	# 						color=0x0000ff
	# 						)
	# 				await ctx.send( embed=embed, tts=False)
	# 	else:
	# 		return

################ 분배 결과 출력 ################
	@client.command(name=command[11][0], aliases=command[11][1:])
	async def bunbae_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			separate_money = []
			separate_money = msg.split("：")
			num_sep = floor(int(separate_money[0]))
			cal_tax1 = floor(float(separate_money[1])*0.05)

			real_money = floor(floor(float(separate_money[1])) - cal_tax1)
			cal_tax2 = floor(real_money/num_sep) - floor(float(floor(real_money/num_sep))*0.95)
			if num_sep == 0 :
				await ctx.send('```分配人数が０です。正しく入力してください。```', tts=False)
			else :
				embed = discord.Embed(
					title = "----- 分配結果！ -----",
					description= '```１次税金 : ' + str(cal_tax1) + '\n一次精算金額 : ' + str(real_money) + '\n分配対象者の取引所登録金額 : ' + str(int(real_money/num_sep)) + '\n２次税金 : ' + str(cal_tax2) + '\n一人あたりの実質精算金額 : ' + str(int(float(int(real_money/num_sep))*0.95)) + '```',
					color=0xff00ff
					)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 사다리 결과 출력 ################
	@client.command(name=command[12][0], aliases=command[12][1:])
	async def ladder_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[8]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			ladder = []
			ladder = msg.split("：")
			try:
				num_cong = int(ladder[0])
				del(ladder[0])
			except ValueError:
				return await ctx.send('```抽選人数は数字で入力してください。\nex)！抽選：１：A：B：C ...```')
			await LadderFunc(num_cong, ladder, ctx)
		else:
			return

	################ 정산확인 ################
	# @client.command(name=command[13][0], aliases=command[13][1:])
	# async def jungsan_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[11]:
	# 		msg = ctx.message.content[len(ctx.invoked_with)+1:]
	# 		if basicSetting[10] !="" and basicSetting[12] !="" and basicSetting[14] !="" and basicSetting[15] !="" and basicSetting[16] !=""  :
	# 			SearchID = msg
	# 			gc = gspread.authorize(credentials)
	# 			wks = gc.open(basicSetting[12]).worksheet(basicSetting[14])

	# 			wks.update_acell(basicSetting[15], SearchID)

	# 			result = wks.acell(basicSetting[16]).value

	# 			embed = discord.Embed(
	# 					description= '```' + SearchID + ' 님이 받을 다이야는 ' + result + ' 다이야 입니다.```',
	# 					color=0xff00ff
	# 					)
	# 			await ctx.send(embed=embed, tts=False)
	# 	else:
	# 		return

	################ 보스타임 일괄 설정 ################
	@client.command(name=command[14][0], aliases=command[14][1:])
	async def allBossInput_(ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		global bossMungTime
		global bossAutoMungCnt
		global bossAutoMungTime

		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(bossNum):
				tmp_msg = msg
				if len(tmp_msg) > 3 :
					if tmp_msg.find(':') != -1 :
						chkpos = tmp_msg.find(':')
						hours1 = tmp_msg[chkpos-2:chkpos]
						minutes1 = tmp_msg[chkpos+1:chkpos+3]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						chkpos = len(tmp_msg)-2
						hours1 = tmp_msg[chkpos-2:chkpos]
						minutes1 = tmp_msg[chkpos:chkpos+2]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
				else:
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = now2

				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				#bossMungCnt[i] = 1
				bossAutoMungCnt[i] = 1
				bossAutoMungTime[i] = []

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))

				bossAutoMungTime[i] = tmp_now.strftime('%Y-%m-%d %H:%M')

				if tmp_now < now2 :
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						#bossMungCnt[i] = bossMungCnt[i] + 1
						bossAutoMungCnt[i] = bossAutoMungCnt[i] + 1
					now2 = tmp_now
					#bossMungCnt[i] = bossMungCnt[i] - 1
					bossAutoMungCnt[i] = bossAutoMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

				tmp_bossTime[i] = bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

			await dbSave()
			await dbLoad()
			await dbSave()

			await ctx.send('<データの一括入力が完了しました。>', tts=False)
			print ("<보스 일괄 입력 완료>")
		else:
			return


	################ 가장 근접한 보스타임 출력 ################
	# @client.command(name=command[15][0], aliases=command[15][1:])
	# async def nearTimeBoss_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		checkTime = datetime.datetime.now() + datetime.timedelta(days=1, hours = int(basicSetting[0]))

	# 		datelist = []
	# 		datelist2 = []
	# 		ouput_bossData = []
	# 		aa = []
	# 		sorted_datelist = []

	# 		for i in range(bossNum):
	# 			if bossMungFlag[i] != True and bossTimeString[i] != '99:99:99' :
	# 				datelist2.append(bossTime[i])

	# 		for i in range(fixed_bossNum):
	# 			if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
	# 				datelist2.append(fixed_bossTime[i])

	# 		datelist = list(set(datelist2))

	# 		for i in range(bossNum):
	# 			if bossMungFlag[i] != True :
	# 				aa.append(bossData[i][0])		                 #output_bossData[0] : 보스명
	# 				aa.append(bossTime[i])                           #output_bossData[1] : 시간
	# 				aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
	# 				ouput_bossData.append(aa)
	# 			aa = []

	# 		for i in range(fixed_bossNum):
	# 			aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
	# 			aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
	# 			aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)
	# 			ouput_bossData.append(aa)
	# 			aa = []

	# 		tmp_sorted_datelist = sorted(datelist)

	# 		for i in range(len(tmp_sorted_datelist)):
	# 			if checkTime > tmp_sorted_datelist[i]:
	# 				sorted_datelist.append(tmp_sorted_datelist[i])

	# 		if len(sorted_datelist) == 0:
	# 			await ctx.send( '<보스타임 정보가 없습니다.>', tts=False)
	# 		else :
	# 			result_lefttime = ''

	# 			if len(sorted_datelist) > int(basicSetting[9]):
	# 				for j in range(int(basicSetting[9])):
	# 					for i in range(len(ouput_bossData)):
	# 						if sorted_datelist[j] == ouput_bossData[i][1]:
	# 							leftTime = ouput_bossData[i][1] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

	# 							total_seconds = int(leftTime.total_seconds())
	# 							hours, remainder = divmod(total_seconds,60*60)
	# 							minutes, seconds = divmod(remainder,60)

	# 							result_lefttime += '다음 ' + ouput_bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
	# 			else :
	# 				for j in range(len(sorted_datelist)):
	# 					for i in range(len(ouput_bossData)):
	# 						if sorted_datelist[j] == ouput_bossData[i][1]:
	# 							leftTime = ouput_bossData[i][1] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

	# 							total_seconds = int(leftTime.total_seconds())
	# 							hours, remainder = divmod(total_seconds,60*60)
	# 							minutes, seconds = divmod(remainder,60)

	# 							result_lefttime += '다음 ' + ouput_bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
	# 			embed = discord.Embed(
	# 				description= result_lefttime,
	# 				color=0xff0000
	# 				)
	# 			await ctx.send( embed=embed, tts=False)
	# 	else:
	# 		return

	################ 음성파일 생성 후 재생 ################
	# @client.command(name=command[16][0], aliases=command[16][1:])
	# async def playText_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		msg = ctx.message.content[len(ctx.invoked_with)+1:]
	# 		sayMessage = msg
	# 		await MakeSound(ctx.message.author.display_name +'님이, ' + sayMessage, './sound/say')
	# 		await ctx.send("```<" + ctx.author.display_name + ">님이 \"" + sayMessage + "\"```", tts=False)
	# 		await PlaySound(voice_client1, './sound/say.wav')
	# 	else:
	# 		return

	################ 리젠시간 출력 ################
	@client.command(name=command[17][0], aliases=command[17][1:])
	async def regenTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send(embed=regenembed, tts=False)
		else:
			return

	################ 현재시간 확인 ################
	@client.command(name=command[18][0], aliases=command[18][1:])
	async def currentTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			curruntTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
			await ctx.send('なう(' + curruntTime.strftime('%Y-%m-%d') + ' ' + curruntTime.strftime('%H:%M:%S') + ')', tts=False)
		else:
			return

	################ 공지 등록/확인 ################
	# @client.command(name=command[19][0], aliases=command[19][1:])
	# async def notice_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		msg = ctx.message.content.split(" ")
	# 		if len(msg) > 1:
	# 			sayMessage = " ".join(msg[1:])
	# 			contents = repo.get_contents("notice.ini")
	# 			repo.update_file(contents.path, "notice 등록", sayMessage, contents.sha)
	# 			await ctx.send( '<공지 등록완료>', tts=False)
	# 		else:
	# 			notice_initdata = repo.get_contents("notice.ini")
	# 			notice = base64.b64decode(notice_initdata.content)
	# 			notice = notice.decode('utf-8')
	# 			if notice != '' :
	# 				embed = discord.Embed(
	# 						description= str(notice),
	# 						color=0xff00ff
	# 						)
	# 			else :
	# 				embed = discord.Embed(
	# 						description= '```등록된 공지가 없습니다.```',
	# 						color=0xff00ff
	# 						)
	# 			await ctx.send(embed=embed, tts=False)
	# 	else:
	# 		return

	################ 공지 삭제 ################
	# @client.command(name=command[20][0], aliases=command[20][1:])
	# async def noticeDel_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		contents = repo.get_contents("notice.ini")
	# 		repo.update_file(contents.path, "notice 삭제", '', contents.sha)
	# 		await ctx.send( '<공지 삭제완료>', tts=False)
	# 	else:
	# 		return

	################ 봇 상태메세지 변경 ################
	# @client.command(name=command[21][0], aliases=command[21][1:])
	# async def botStatus_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		msg = ctx.message.content[len(ctx.invoked_with)+1:]
	# 		sayMessage = msg
	# 		await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=sayMessage, type=1), afk = False)
	# 		await ctx.send( '<상태메세지 변경완료>', tts=False)
	# 	else:
	# 		return

	################ 보스타임 출력 ################
	@client.command(name=command[22][0], aliases=command[22][1:])
	async def bossTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []

			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1000 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + '、'
				else :
					aa.append(bossData[i][8])		                             #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                             #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M'))           #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))
						aa.append('-')	                                       #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                                 #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M'))               #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M:%S'))
						aa.append('+')	                                       #output_bossData[3] : +
					aa.append(bossData[i][2])                                #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                               #output_bossData[5] : 멍/미입력횟수
					if bossMungTime[i] != '1987-09-12 10:30' :
						aa.append(' [' + bossMungTime[i][5:] + ']')	           #output_bossData[6] : 멍/미입력시간
					else :
						aa.append('')	                                         #output_bossData[6] : 멍/미입력시간
					aa.append(bossAutoMungCnt[i])	                           #output_bossData[7] : 자동 멍/미입력횟수
					if bossAutoMungTime[i] != '1987-09-12 10:30' :
						aa.append(' E[' + bossAutoMungTime[i][5:] + ']')	     #output_bossData[8] : 자동 멍/미입력시간
					else :
						aa.append('')	                                         #output_bossData[8] : 자동 멍/미입력시간
					if bossData[i][6] != '' :
						aa.append('<' + bossData[i][6] + '>')	                 #output_bossData[9] : 메세지
					else :
						aa.append('')	                                         #output_bossData[9] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][11])                     #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))       #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(fixed_bossTime[i].strftime('%H:%M'))
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
				aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
				aa.append("")	                                       #output_bossData[6] : 멍/미입력시간
				aa.append(0)                                         #output_bossData[7] : 자동 멍/미입력횟수
				aa.append("")	                                       #output_bossData[8] : 자동 멍/미입력시간
				aa.append("")                                        #output_bossData[9] : 메세지
				ouput_bossData.append(aa)
				aa = []

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][7] == 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][9] + '\n'
							else :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + ' (未：' + str(ouput_bossData[i][7]) + '回' + str(ouput_bossData[i][8]) +  ')' + ' ' + ouput_bossData[i][9] + '\n'
						else :
							if ouput_bossData[i][5] != 0 and ouput_bossData[i][7] != 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R (pass：' + str(ouput_bossData[i][5]) + '回' + str(ouput_bossData[i][6]) +  '、未：' + str(ouput_bossData[i][7]) + '回' + str(ouput_bossData[i][8]) +  ')' + ' ' + ouput_bossData[i][9] + '\n'
							elif ouput_bossData[i][5] != 0 and ouput_bossData[i][7] == 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R (pass：' + str(ouput_bossData[i][5]) + '回' + str(ouput_bossData[i][6]) +  ')' + ' ' + ouput_bossData[i][9] + '\n'
							elif ouput_bossData[i][5] == 0 and ouput_bossData[i][7] != 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R (未：' + str(ouput_bossData[i][7]) + '回' + str(ouput_bossData[i][8]) +  ')' + ' ' + ouput_bossData[i][9] + '\n'
							else :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R ' + ouput_bossData[i][9] + '\n'

			if len(boss_information) == 1 and len(tmp_boss_information) == 1:
				###########################
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- ボス湧き情報 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				embed.add_field(
						name="----- 確認されていないボス -----",
						value= tmp_boss_information[0],
						inline = False
						)
				await ctx.send(embed=embed, tts=False)
			else :
				###########################일반보스출력
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- ボス湧き情報 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				await ctx.send(embed=embed, tts=False)
				for i in range(len(boss_information)-1):
					if len(boss_information[i+1]) != 0:
						boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
					else :
						boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send(embed=embed, tts=False)
				###########################미예약보스출력
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- 確認されていないボス -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send(embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send(embed=embed, tts=False)

			await dbSave()
		else:
			return

	################ 보스타임 출력 (한글) ################
	@client.command(name=command[23][0], aliases=command[23][1:])
	async def bossTime_fixed_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1000 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][9] + '、'
				else :
					aa.append(bossData[i][9])		                             #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                             #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M'))           #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M'))
						aa.append('-')	                                       #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                                 #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M'))               #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M'))
						aa.append('+')	                                       #output_bossData[3] : +
					aa.append(bossData[i][2])                                #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                               #output_bossData[5] : 멍/미입력횟수
					if bossMungTime[i] != '1987-09-12 10:30' :
						aa.append(' [' + bossMungTime[i][5:] + ']')	           #output_bossData[6] : 멍/미입력시간
					else :
						aa.append('')	                                         #output_bossData[6] : 멍/미입력시간
					aa.append(bossAutoMungCnt[i])	                           #output_bossData[7] : 자동 멍/미입력횟수
					if bossAutoMungTime[i] != '1987-09-12 10:30' :
						aa.append(' 컷[' + bossAutoMungTime[i][5:] + ']')	     #output_bossData[8] : 자동 멍/미입력시간
					else :
						aa.append('')	                                         #output_bossData[8] : 자동 멍/미입력시간
					if bossData[i][6] != '' :
						aa.append('<' + bossData[i][6] + '>')	                 #output_bossData[9] : 메세지
					else :
						aa.append('')	                                         #output_bossData[9] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][12])                     #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M'))       #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(fixed_bossTime[i].strftime('%H:%M'))
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
				aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
				aa.append("")	                                       #output_bossData[6] : 멍/미입력시간
				aa.append(0)                                         #output_bossData[7] : 자동 멍/미입력횟수
				aa.append("")	                                       #output_bossData[8] : 자동 멍/미입력시간
				aa.append("")                                        #output_bossData[9] : 메세지
				ouput_bossData.append(aa)
				aa = []

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][7] == 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][9] + '\n'
							else :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + ' (미：' + str(ouput_bossData[i][7]) + '회' + str(ouput_bossData[i][8]) + ')' + ' ' + ouput_bossData[i][9] + '\n'
						else :
							if ouput_bossData[i][5] != 0 and ouput_bossData[i][7] != 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R (멍：' + str(ouput_bossData[i][5]) + '회' + str(ouput_bossData[i][6]) + '、미：' + str(ouput_bossData[i][7]) + '회' + str(ouput_bossData[i][8]) +  ')' + ' ' + ouput_bossData[i][9] + '\n'
							elif ouput_bossData[i][5] != 0 and ouput_bossData[i][7] == 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R (멍：' + str(ouput_bossData[i][5]) + '회' + str(ouput_bossData[i][6]) + ')' + ' ' + ouput_bossData[i][9] + '\n'
							elif ouput_bossData[i][5] == 0 and ouput_bossData[i][7] != 0 :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R (미：' + str(ouput_bossData[i][7]) + '회' + str(ouput_bossData[i][8]) + ')' + ' ' + ouput_bossData[i][9] + '\n'
							else :
								boss_information[cnt] += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + '　' + ouput_bossData[i][0] + '/R ' + ouput_bossData[i][9] + '\n'

			if len(boss_information) == 1 and len(tmp_boss_information) == 1:
				###########################
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				embed.add_field(
						name="----- 미확인 -----",
						value= tmp_boss_information[0],
						inline = False
						)

				await ctx.send(embed=embed, tts=False)
			else :
				###########################일반보스출력
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				await ctx.send(embed=embed, tts=False)
				for i in range(len(boss_information)-1):
					if len(boss_information[i+1]) != 0:
						boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
					else :
						boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send(embed=embed, tts=False)
				###########################미예약보스출력
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- 미확인 -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send(embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send(embed=embed, tts=False)

			await dbSave()
		else:
			return

	################ 보스타임 출력(고정보스포함) ################
	# @client.command(name=command[23][0], aliases=command[23][1:])
	# async def bossTime_fixed_(ctx):
	# 	if ctx.message.channel.id == basicSetting[7]:
	# 		datelist = []
	# 		datelist2 = []
	# 		ouput_bossData = []
	# 		aa = []
	# 		fixed_datelist = []

	# 		for i in range(bossNum):
	# 			if bossMungFlag[i] == True :
	# 				datelist2.append(tmp_bossTime[i])
	# 			else :
	# 				datelist2.append(bossTime[i])

	# 		datelist = list(set(datelist2))

	# 		tmp_boss_information = []
	# 		tmp_cnt = 0
	# 		tmp_boss_information.append('')

	# 		for i in range(bossNum):
	# 			if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
	# 				if len(tmp_boss_information[tmp_cnt]) > 1800 :
	# 					tmp_boss_information.append('')
	# 					tmp_cnt += 1
	# 				tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
	# 			else :
	# 				aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
	# 				if bossMungFlag[i] == True :
	# 					aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
	# 					aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M'))
	# 					aa.append('-')	                                 #output_bossData[3] : -
	# 				else :
	# 					aa.append(bossTime[i])                           #output_bossData[1] : 시간
	# 					aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M'))
	# 					aa.append('+')	                                 #output_bossData[3] : +
	# 				aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
	# 				aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
	# 				aa.append(bossData[i][6])	                         #output_bossData[6] : 메세지
	# 				ouput_bossData.append(aa)
	# 				aa = []

	# 		for i in range(fixed_bossNum):
	# 			fixed_datelist.append(fixed_bossTime[i])

	# 		fixed_datelist = list(set(fixed_datelist))

	# 		fixedboss_information = []
	# 		cntF = 0
	# 		fixedboss_information.append('')

	# 		for timestring1 in sorted(fixed_datelist):
	# 			if len(fixedboss_information[cntF]) > 1800 :
	# 				fixedboss_information.append('')
	# 				cntF += 1
	# 			for i in range(fixed_bossNum):
	# 				if timestring1 == fixed_bossTime[i]:
	# 					if (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).strftime('%Y-%m-%d') == fixed_bossTime[i].strftime('%Y-%m-%d'):
	# 						tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M:%S') #초빼기 : tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M')
	# 					else:
	# 						tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M:%S') #초빼기 : tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M')
	# 					fixedboss_information[cntF] = fixedboss_information[cntF] + tmp_timeSTR + ' : ' + fixed_bossData[i][0] + '\n'

	# 		boss_information = []
	# 		cnt = 0
	# 		boss_information.append('')

	# 		for timestring in sorted(datelist):
	# 			if len(boss_information[cnt]) > 1800 :
	# 				boss_information.append('')
	# 				cnt += 1
	# 			for i in range(len(ouput_bossData)):
	# 				if timestring == ouput_bossData[i][1]:
	# 					if ouput_bossData[i][4] == '0' :
	# 						if ouput_bossData[i][5] == 0 :
	# 							boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
	# 						else :
	# 							boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
	# 					else :
	# 						if ouput_bossData[i][5] == 0 :
	# 							boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
	# 						else :
	# 							boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'

	# 		###########################고정보스출력
	# 		if len(fixedboss_information[0]) != 0:
	# 			fixedboss_information[0] = "```diff\n" + fixedboss_information[0] + "\n```"
	# 		else :
	# 			fixedboss_information[0] = '``` ```'

	# 		embed = discord.Embed(
	# 				title = "----- 고 정 보 스 -----",
	# 				description= fixedboss_information[0],
	# 				color=0x0000ff
	# 				)
	# 		await ctx.send( embed=embed, tts=False)
	# 		for i in range(len(fixedboss_information)-1):
	# 			if len(fixedboss_information[i+1]) != 0:
	# 				fixedboss_information[i+1] = "```diff\n" + fixedboss_information[i+1] + "\n```"
	# 			else :
	# 				fixedboss_information[i+1] = '``` ```'

	# 			embed = discord.Embed(
	# 					title = '',
	# 					description= fixedboss_information[i+1],
	# 					color=0x0000ff
	# 					)
	# 			await ctx.send( embed=embed, tts=False)

	# 		###########################일반보스출력
	# 		if len(boss_information[0]) != 0:
	# 			boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
	# 		else :
	# 			boss_information[0] = '``` ```'

	# 		embed = discord.Embed(
	# 				title = "----- 보스탐 정보 -----",
	# 				description= boss_information[0],
	# 				color=0x0000ff
	# 				)
	# 		await ctx.send( embed=embed, tts=False)
	# 		for i in range(len(boss_information)-1):
	# 			if len(boss_information[i+1]) != 0:
	# 				boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
	# 			else :
	# 				boss_information[i+1] = '``` ```'

	# 			embed = discord.Embed(
	# 					title = '',
	# 					description= boss_information[i+1],
	# 					color=0x0000ff
	# 					)
	# 			await ctx.send( embed=embed, tts=False)

	# 		###########################미예약보스출력
	# 		if len(tmp_boss_information[0]) != 0:
	# 			if len(tmp_boss_information) == 1 :
	# 				tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
	# 			else:
	# 				tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
	# 		else :
	# 			tmp_boss_information[0] = '``` ```'

	# 		embed = discord.Embed(
	# 			title = "----- 미예약 보스 -----",
	# 			description= tmp_boss_information[0],
	# 			color=0x0000ff
	# 			)
	# 		await ctx.send( embed=embed, tts=False)
	# 		for i in range(len(tmp_boss_information)-1):
	# 			if len(tmp_boss_information[i+1]) != 0:
	# 				if i == len(tmp_boss_information)-2:
	# 					tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
	# 				else:
	# 					tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
	# 			else :
	# 				tmp_boss_information[i+1] = '``` ```'

	# 			embed = discord.Embed(
	# 					title = '',
	# 					description= tmp_boss_information[i+1],
	# 					color=0x0000ff
	# 					)
	# 			await ctx.send( embed=embed, tts=False)

	# 		await dbSave()
	# 		await kill_list_Save()
	# 	else:
	# 		return


	################ 경주 ################
	@client.command(name=command[24][0], aliases=command[24][1:])
	async def race_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			race_info = []
			fr = []
			racing_field = []
			str_racing_field = []
			cur_pos = []
			race_val = []
			random_pos = []
			racing_result = []
			output = ':camera: :camera: :camera:  楽しいレーシング!  :camera: :camera: :camera:\n'
			#racing_unit = [':giraffe:', ':elephant:', ':tiger2:', ':hippopotamus:', ':crocodile:',':leopard:',':ox:', ':sheep:', ':pig2:',':dromedary_camel:',':dragon:',':rabbit2:'] #동물스킨
			#racing_unit = [':red_car:', ':taxi:', ':bus:', ':trolleybus:', ':race_car:', ':police_car:', ':ambulance:', ':fire_engine:', ':minibus:', ':truck:', ':articulated_lorry:', ':tractor:', ':scooter:', ':manual_wheelchair:', ':motor_scooter:', ':auto_rickshaw:', ':blue_car:', ':bike:', ':helicopter:', ':steam_locomotive:']  #탈것스킨
			#random.shuffle(racing_unit)
			racing_member = msg.split("：")

			racing_unit = []

			emoji = discord.Emoji
			emoji = ctx.message.guild.emojis

			for j in range(len(tmp_racing_unit)):
				racing_unit.append(':' + tmp_racing_unit[j] + ':')
				for i in range(len(emoji)):
					if emoji[i].name == tmp_racing_unit[j].strip(":"):
						racing_unit[j] = '<:' + tmp_racing_unit[j] + ':' + str(emoji[i].id) + '>'

			random.shuffle(racing_unit)

			field_size = 60
			tmp_race_tab = 35 - len(racing_member)
			if len(racing_member) <= 1:
				await ctx.send('人数が一人以下です。')
				return
			elif len(racing_member) >= 13:
				await ctx.send('人数が１２人を超えました。')
				return
			else :
				race_val = random.sample(range(tmp_race_tab, tmp_race_tab+len(racing_member)), len(racing_member))
				random.shuffle(race_val)
				for i in range(len(racing_member)):
					fr.append(racing_member[i])
					fr.append(racing_unit[i])
					fr.append(race_val[i])
					race_info.append(fr)
					fr = []
					for i in range(field_size):
						fr.append(" ")
					racing_field.append(fr)
					fr = []

				for i in range(len(racing_member)):
					racing_field[i][0] = "|"
					racing_field[i][field_size-2] = race_info[i][1]
					if len(race_info[i][0]) > 5:
						racing_field[i][field_size-1] = "| " + race_info[i][0][:5] + '..'
					else:
						racing_field[i][field_size-1] = "| " + race_info[i][0]
					str_racing_field.append("".join(racing_field[i]))
					cur_pos.append(field_size-2)

				for i in range(len(racing_member)):
					output +=  str_racing_field[i] + '\n'

				result_race = await ctx.send(output + ':traffic_light: 3!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 2!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 1!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':checkered_flag:  スタート！')

				for i in range(len(racing_member)):
					test = random.sample(range(2,field_size-2), race_info[i][2])
					while len(test) != tmp_race_tab + len(racing_member)-1 :
						test.append(1)
					test.append(1)
					test.sort(reverse=True)
					random_pos.append(test)

				for j in range(len(random_pos[0])):
					if j%2 == 0:
						output =  ':camera: :camera_with_flash: :camera:  楽しいレーシング！  :camera_with_flash: :camera: :camera_with_flash:\n'
					else :
						output =  ':camera_with_flash: :camera: :camera_with_flash:  楽しいレーシング！  :camera: :camera_with_flash: :camera:\n'
					str_racing_field = []
					for i in range(len(racing_member)):
						temp_pos = cur_pos[i]
						racing_field[i][random_pos[i][j]], racing_field[i][temp_pos] = racing_field[i][temp_pos], racing_field[i][random_pos[i][j]]
						cur_pos[i] = random_pos[i][j]
						str_racing_field.append("".join(racing_field[i]))

					await asyncio.sleep(1)

					for i in range(len(racing_member)):
						output +=  str_racing_field[i] + '\n'

					await result_race.edit(content = output + ':checkered_flag:  スタート！')

				for i in range(len(racing_field)):
					fr.append(race_info[i][0])
					fr.append((race_info[i][2]) - tmp_race_tab + 1)
					racing_result.append(fr)
					fr = []

				result = sorted(racing_result, key=lambda x: x[1])

				result_str = '\n'
				for i in range(len(result)):
					if result[i][1] == 1:
						result[i][1] = ':first_place:'
					elif result[i][1] == 2:
						result[i][1] = ':second_place:'
					elif result[i][1] == 3:
						result[i][1] = ':third_place:'
					elif result[i][1] == 4:
						result[i][1] = ':four:'
					elif result[i][1] == 5:
						result[i][1] = ':five:'
					elif result[i][1] == 6:
						result[i][1] = ':six:'
					elif result[i][1] == 7:
						result[i][1] = ':seven:'
					elif result[i][1] == 8:
						result[i][1] = ':eight:'
					elif result[i][1] == 9:
						result[i][1] = ':nine:'
					elif result[i][1] == 10:
						result[i][1] = ':keycap_ten:'
					else:
						result[i][1] = ':x:'
					result_str += result[i][1] + "  " + result[i][0] + "  "

				#print(result)
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':tada: レーシング終了！\n' + result_str)
		else:
			return

	################ 보탐봇 입장 ################
	@client.command(name=command[25][0], aliases=command[25][1:])
	async def set_channel_(ctx):
		global basicSetting

		msg = ctx.message.content[len(ctx.invoked_with)+1:]
		channel = ctx.message.channel.id #메세지가 들어온 채널 ID

		if msg == '사다리' : #사다리 채널 설정
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')

			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('ladderchannel'):
					inputData_textCH[i] = 'ladderchannel = ' + str(channel) + '\r'
					basicSetting[8] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			await ctx.send(f'<사다리채널 [{ctx.message.channel.name}] 설정완료>', tts=False)
			print(f'<사다리채널 [{ctx.message.channel.name}] 설정완료>')
		# elif msg == '정산' :
		# 	inidata_textCH = repo.get_contents("test_setting.ini")
		# 	file_data_textCH = base64.b64decode(inidata_textCH.content)
		# 	file_data_textCH = file_data_textCH.decode('utf-8')
		# 	inputData_textCH = file_data_textCH.split('\n')

		# 	for i in range(len(inputData_textCH)):
		# 		if inputData_textCH[i].startswith('jungsanchannel'):
		# 			inputData_textCH[i] = 'jungsanchannel = ' + str(channel) + '\r'
		# 			basicSetting[11] = channel
		# 	result_textCH = '\n'.join(inputData_textCH)

		# 	contents = repo.get_contents("test_setting.ini")
		# 	repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

		# 	await ctx.send(f'<정산채널 [{ctx.message.channel.name}] 설정완료>', tts=False)
		# 	print(f'<정산채널 [{ctx.message.channel.name}] 설정완료>')
		elif msg == '경주' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')

			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('racingchannel'):
					inputData_textCH[i] = 'racingchannel = ' + str(channel) + '\r'
					basicSetting[19] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			await ctx.send(f'<경주채널 [{ctx.message.channel.name}] 설정완료>', tts=False)
			print(f'<경주채널 [{ctx.message.channel.name}] 설정완료>')
		else :
			await ctx.send(f'```올바른 명령어를 입력해주세요.```', tts=False)

	################ ?????????????? ################
	# @client.command(name='!오빠')
	# async def brother1_(ctx):
	# 	await PlaySound(voice_client1, './sound/오빠.mp3')

	# @client.command(name='!언니')
	# async def sister_(ctx):
	# 	await PlaySound(voice_client1, './sound/언니.mp3')

	# @client.command(name='!형')
	# async def brother2_(ctx):
	# 	await PlaySound(voice_client1, './sound/형.mp3')

	# @client.command(name='!TJ', aliases=['!tj'])
	# async def TJ_(ctx):
	# 	resultTJ = random.randrange(1,9)
	# 	await PlaySound(voice_client1, './sound/TJ' + str(resultTJ) +'.mp3')

	@client.command(name='！クベーラ')
	async def test_msg_1_(ctx):
		await ctx.send('全てのデータを削除しました。', tts=False)

	# Bot
	@client.command(name='！愛してる')
	async def test_msg_2_(ctx):
		await ctx.send('私も。', tts=False)
	@client.command(name='！KISSME')
	async def test_msg_3_(ctx):
		await ctx.send('ちゅー', tts=False)

	# Liberte
	@client.command(name='！バロ')
	async def test_msg_5_(ctx):
		await ctx.send('「家庭的でエロい子が好き。」', tts=False)
	@client.command(name='バロエンド')
	async def test_msg_6_(ctx):
		await ctx.send('バロの湧き時間です。（確定）', tts=False)
	# WIZ
	@client.command(name='！かるぼなーら')
	async def test_msg_7_(ctx):
		await ctx.send('( っ`-´c)ｷﾞﾘｨ', tts=False)
	@client.command(name='！ちゅみ')
	async def test_msg_8_(ctx):
		await ctx.send('(っ`ω´c)ｷﾞﾘｨ', tts=False)
	# DE
	@client.command(name='！煌雲')
	async def test_msg_9_(ctx):
		await ctx.send('ABおめでとう！', tts=False)
	@client.command(name='！弘雲')
	async def test_msg_9_(ctx):
		await ctx.send('ABおめでとう！', tts=False)
	# 銃士
	@client.command(name='！ラピッドマン')
	async def test_msg_10_(ctx):
		await ctx.send('スタンおめでとう！', tts=False)
	@client.command(name='！やまだまん')
	async def test_msg_10_(ctx):
		await ctx.send('スタンおめでとう！', tts=False)
	# ナイト
	@client.command(name='!火山')
	async def test_msg_11_(ctx):
		await ctx.send('리베에서 재밌게 놀아봐요! ke！', tts=False)
	@client.command(name='！火山')
	async def test_msg_11_(ctx):
		await ctx.send('리베에서 재밌게 놀아봐요! ke！', tts=False)
	@client.command(name='！PAKA')
	async def test_msg_12_(ctx):
		await ctx.send('안녕! バカ！', tts=False)
	@client.command(name='！ファヌエル')
	async def test_msg_13_(ctx):
		await ctx.send('リベルテへようこそ！', tts=False)
	# ELF

	# 田中家
	@client.command(name='！ロンドン5')
	async def test_msg_14_(ctx):
		await ctx.send('ロンさん大好き！', tts=False)

	# ガイジパーク
	@client.command(name='がば')
	async def test_msg_15_(ctx):
		await ctx.send('愛してる', tts=False)
	@client.command(name='！がば')
	async def test_msg_15_(ctx):
		await ctx.send('(機械的に) 愛してる', tts=False)
	@client.command(name='！れお')
	async def test_msg_16_(ctx):
		await ctx.send('変態', tts=False)

	@client.event
	async def on_command_error(ctx, error):
		if isinstance(error, CommandNotFound):
			return
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			return
		raise error

	# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
	@client.event
	async def on_message(msg):
		await client.wait_until_ready()
		if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
			return None #동작하지 않고 무시합니다.

		ori_msg = msg

		global channel

		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		global bossMungTime
		global bossAutoMungCnt
		global bossAutoMungTime

		#voice:global voice_client1

		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type

		global chflg
		global LoadChk

		global indexFixedBossname
		global FixedBossDateData

		global gc #정산
		global credentials	#정산

		global regenembed
		global command

		id = msg.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.

		if chflg == 1 :
			if client.get_channel(basicSetting[7]).id == msg.channel.id:
				channel = basicSetting[7]
				message = msg

				hello = message.content

				for i in range(bossNum):
					################ 보스 컷처리 ################
					if message.content.startswith(bossData[i][0] +'cut'): # 컷
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''

						tmp_msg = bossData[i][0] +'cut' # 컷
						if len(hello) > len(tmp_msg) + 3 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1), second=now2.second, microsecond=now2.microsecond)
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1), second=now2.second, microsecond=now2.microsecond)
						else:
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = now2

						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0
						bossMungTime[i] = '1987-09-12 10:30'
						bossAutoMungCnt[i] = 0

						if tmp_now > now2 :
							tmp_now = tmp_now + datetime.timedelta(days=int(-1))

						bossAutoMungTime[i] = tmp_now.strftime('%Y-%m-%d %H:%M')

						if tmp_now < now2 :
							deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							while now2 > tmp_now :
								tmp_now = tmp_now + deltaTime
								#bossMungCnt[i] = bossMungCnt[i] + 1
								bossAutoMungCnt[i] = bossAutoMungCnt[i] + 1
							now2 = tmp_now
							#bossMungCnt[i] = bossMungCnt[i] - 1
							bossAutoMungCnt[i] = bossAutoMungCnt[i] - 1
						else :
							now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

						tmp_bossTime[i] = bossTime[i] = nextTime = now2
						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '```次、' + bossData[i][0] + 'の湧き時間は ' + bossTimeString[i] + ' です。```',
								color=0xff0000
								)
						await client.get_channel(channel).send(embed=embed, tts=False)

					################ 보스 멍 처리 ################
					if message.content.startswith(bossData[i][0] +'pass'):
						################ 미입력 보스 ################
						if bossData[i][2] == '0' :
							await client.get_channel(channel).send('```' + bossData[i][0] + 'は確定湧きボスです。```', tts=False)
						################ 멍 보스 ################
						else :
							if hello.find('  ') != -1 :
								bossData[i][6] = hello[hello.find('  ')+2:]
								hello = hello[:hello.find('  ')]
							else:
								bossData[i][6] = ''

							tmp_msg = bossData[i][0] +'pass'
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

							if len(hello) > len(tmp_msg) + 3 :
								temptime = tmp_now
								if hello.find(':') != -1 :
									chkpos = hello.find(':')
									hours1 = hello[chkpos-2:chkpos]
									minutes1 = hello[chkpos+1:chkpos+3]
									temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
								else:
									chkpos = len(hello)-2
									hours1 = hello[chkpos-2:chkpos]
									minutes1 = hello[chkpos:chkpos+2]
									temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))

								bossMungCnt[i] = 0
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False

								if temptime > tmp_now :
									temptime = temptime + datetime.timedelta(days=int(-1))

								bossMungTime[i] = temptime.strftime('%Y-%m-%d %H:%M')

								if temptime < tmp_now :
									deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
									while temptime < tmp_now :
										temptime = temptime + deltaTime
										bossMungCnt[i] = bossMungCnt[i] + 1

								tmp_bossTime[i] = bossTime[i] = temptime

								tmp_bossTimeString[i] = bossTimeString[i] = temptime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = temptime.strftime('%Y-%m-%d')
								embed = discord.Embed(
										description= '```次、' + bossData[i][0] + 'の湧き時間は ' + bossTimeString[i] + ' です。```',
										color=0xff0000
										)
								await client.get_channel(channel).send(embed=embed, tts=False)
							else:
								if tmp_bossTime[i] < tmp_now :

									nextTime = tmp_bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									bossMungCnt[i] = bossMungCnt[i] + 1
									bossMungTime[i] = tmp_now.strftime('%Y-%m-%d %H:%M')

									tmp_bossTime[i] = bossTime[i] = nextTime

									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									embed = discord.Embed(
											description= '```次、' + bossData[i][0] + 'の湧き時間は ' + bossTimeString[i] + ' です。```',
											color=0xff0000
											)
									await client.get_channel(channel).send(embed=embed, tts=False)
								else:
									await client.get_channel(channel).send('```まだ' + bossData[i][0] + 'の湧き時間ではありません。次の時間に確認してみてください。[' + bossTimeString[i] + ']```', tts=False)

					################ 예상 보스 타임 입력 ################
					if message.content.startswith(bossData[i][0] +'予想'):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''

						tmp_msg = bossData[i][0] +'予想'
						if len(hello) > len(tmp_msg) + 3 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))

							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = 0
							bossMungTime[i] = '1987-09-12 10:30'
							bossAutoMungCnt[i] = 0

							if tmp_now < now2 :
								tmp_now = tmp_now + datetime.timedelta(days=int(1))

							bossAutoMungTime[i] = tmp_now.strftime('%Y-%m-%d %H:%M')

							tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '```次、' + bossData[i][0] + 'の湧き時間は ' + bossTimeString[i] + ' です。```',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
						else:
							await client.get_channel(channel).send('```' + bossData[i][0] +'の予想湧き時間を入力してください。```', tts=False)

					################ 보스타임 삭제 ################
					if message.content == bossData[i][0] +'削除':
						bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
						tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
						bossTimeString[i] = '99:99:99'
						bossDateString[i] = '9999-99-99'
						tmp_bossTimeString[i] = '99:99:99'
						tmp_bossDateString[i] = '9999-99-99'
						bossFlag[i] = (False)
						bossFlag0[i] = (False)
						bossMungFlag[i] = (False)
						bossMungCnt[i] = 0
						bossMungTime[i] = '1987-09-12 10:30'
						bossAutoMungCnt[i] = 0
						bossAutoMungTime[i] = '1987-09-12 10:30'
						await client.get_channel(channel).send('<' + bossData[i][0] + 'の時間記録を削除しました。>', tts=False)
						await dbSave()
						print ('<' + bossData[i][0] + ' 삭제완료>')

					################ 보스별 메모 ################
					if message.content.startswith(bossData[i][0] +'：') or message.content.startswith(bossData[i][0] +':') or message.content.startswith(bossData[i][0] +'　') or message.content.startswith(bossData[i][0] +' '):
						tmp_msg = bossData[i][0] + '：'
						bossData[i][6] = hello[len(tmp_msg):]
						await client.get_channel(channel).send('<' + bossData[i][0] + 'にメモ [ ' + bossData[i][6] + ' ] を登録しました。>', tts=False)

					if message.content.startswith(bossData[i][0] +'メモ削除'):
						bossData[i][6] = ''
						await client.get_channel(channel).send('<' + bossData[i][0] + 'のメモを削除しました。>', tts=False)

		await client.process_commands(ori_msg)

	client.loop.create_task(task())
	try:
		client.loop.run_until_complete(client.start(access_token))
	except SystemExit:
		handle_exit()
	except KeyboardInterrupt:
		handle_exit()
	#client.loop.close()
	#print("Program ended")
	#break

	print("Bot restarting")
	client = discord.Client(loop=client.loop)
	client = commands.Bot(command_prefix="", help_command = None, description='KuberaBot')
