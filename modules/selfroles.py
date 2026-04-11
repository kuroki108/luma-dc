# Selfrole System / Dropdown Menu
import discord


class RoleSelect(discord.ui.Select):

    multi: bool = False

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Dieser Befehl kann nur in einem Server verwendet werden.", ephemeral=True)
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message("Member nicht gefunden.", ephemeral=True)
            return

        await interaction.response.edit_message(view=self.view)

        # Rollen per ID suchen statt per Name
        all_group_roles = [
            role for option in self.options
            if (role := guild.get_role(int(option.value)))
        ]

        if self.multi:
            selected_roles = [
                role for role_id in self.values
                if (role := guild.get_role(int(role_id)))
            ]
            roles_to_remove = [r for r in all_group_roles if r in member.roles]
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
            if selected_roles:
                await member.add_roles(*selected_roles)
            names = ", ".join(f"**{r.name}**" for r in selected_roles)
            response_text = f"Deine Rollen wurden aktualisiert!\nDu hast jetzt folgende Rollen: {names}" if names else "Alle deine Rollen aus dieser Kategorie wurden entfernt."

        else:
            selected = guild.get_role(int(self.values[0]))
            if selected is None:
                await interaction.followup.send(
                    "Oh! Deine Rolle wurde nicht gefunden.\n"
                    "Bitte melde uns dies über unser Ticketsystem.\nDankeschön!",
                    ephemeral=True
                )
                return
            if selected in member.roles:
                await member.remove_roles(selected)
                response_text = f"Du hast die Rolle **{selected.name}** entfernt."
            else:
                roles_to_remove = [r for r in all_group_roles if r in member.roles]
                if roles_to_remove:
                    await member.remove_roles(*roles_to_remove)
                await member.add_roles(selected)
                response_text = f"Du hast die Rolle **{selected.name}** bekommen!"

        await interaction.followup.send(response_text, ephemeral=True)


class AgeRoles(RoleSelect):

    def __init__(self):
        super().__init__(
            custom_id="select_age",
            placeholder="Alter",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="16 bis 17", value="1490767664333717725"),
                discord.SelectOption(label="18 bis 20",  value="1490767668717027398"),
                discord.SelectOption(label="21 bis 25",  value="1490767673783750666"),
                discord.SelectOption(label="26 bis 30",  value="1490767676291678319"),
                discord.SelectOption(label="31 bis 35",  value="1490767678703407134"),
                discord.SelectOption(label="35 + (Unc)", value="1492074294753366107"),
            ]
        )


class GenderRoles(RoleSelect):

    def __init__(self):
        super().__init__(
            custom_id="select_gender",
            placeholder="Geschlecht",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Männlich", value="1490762838858399774"),  
                discord.SelectOption(label="Weiblich",  value="1490762830088110290"),
                discord.SelectOption(label="Trans",     value="1490767576454791359"),  
            ]
        )


class StateRoles(RoleSelect):

    def __init__(self):
        super().__init__(
            custom_id="select_state",
            placeholder="Bundesland",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Baden-Württemberg",       value="1490767681278836857"),  
                discord.SelectOption(label="Bayern",                  value="1490768166446432296"),   
                discord.SelectOption(label="Berlin",                  value="1490768169801879775"),  
                discord.SelectOption(label="Brandenburg",             value="1490768172943671509"),   
                discord.SelectOption(label="Bremen",                  value="1490768176177221802"),   
                discord.SelectOption(label="Hamburg",                 value="1490768179700699379"),  
                discord.SelectOption(label="Hessen",                  value="1490768183039230094"),              
                discord.SelectOption(label="Mecklenburg-Vorpommern",  value="1490768186889736328"),                
                discord.SelectOption(label="Niedersachsen",           value="1490768194066059294"),                
                discord.SelectOption(label="Nordrhein-Westfalen",     value="1490768195076751420"),                
                discord.SelectOption(label="Rheinland-Pfalz",         value="1490768197903712538"),                
                discord.SelectOption(label="Saarland",                value="1490768203020763249"),                
                discord.SelectOption(label="Sachsen",                 value="1490768206410027241"),                
                discord.SelectOption(label="Sachsen-Anhalt",          value="1490768210167857173"),                
                discord.SelectOption(label="Schleswig-Holstein",      value="1490768213653590166"),                
                discord.SelectOption(label="Thüringen",               value="1490768220347433091"),                
                discord.SelectOption(label="Österreich",              value="1492512050503618650"),                
                discord.SelectOption(label="Schweiz",                 value="1492512090181603582"),            
                ]
        )


class DM_StatusRoles(RoleSelect):

    def __init__(self):
        super().__init__(
            custom_id="select_dm_status",
            placeholder="DM Status",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Dm´s -offen",       value="1490768232326627502"),
                discord.SelectOption(label="Dm´s -anfrage",    value="1490768236403364122"), 
                discord.SelectOption(label="Dm´s -close", value="1490768239855276202"),  
            ]
        )


class PingRoles(RoleSelect):

    multi = True

    def __init__(self):
        super().__init__(
            custom_id="select_ping",
            placeholder="Ping",
            min_values=1,
            max_values=7,
            options=[
                discord.SelectOption(label="Bumper",                    value="1490768258394099712"),  
                discord.SelectOption(label="Umfragen",                  value="1490768261992677498"), 
                discord.SelectOption(label="Neuigkeiten/Ankündigungen", value="1490768266707337286"),  
                discord.SelectOption(label="Giveaways",                 value="1490768271421603870"), 
                discord.SelectOption(label="Events",                    value="1490768275934679282"), 
                discord.SelectOption(label="Minigames",                 value="1490768280410128475"),  
                discord.SelectOption(label="Death Chat",                value="1490768285182988540"), 
            ]
        )


class GamesRoles(RoleSelect):

    multi = True

    def __init__(self):
        super().__init__(
            custom_id="select_games",
            placeholder="Games",
            min_values=1,
            max_values=16,
            options=[
                discord.SelectOption(label="Spielersuche",               value="1490823990564884791"),  
                discord.SelectOption(label="Minecraft",                  value="1490768289956102246"),  
                discord.SelectOption(label="Dead by Daylight",           value="1490768296159477911"),  
                discord.SelectOption(label="Valorant",                   value="1490768300718817280"),  
                discord.SelectOption(label="Phasmophobia",               value="1490768305009721565"),  
                discord.SelectOption(label="Fortnite",                   value="1490768314040057886"),  
                discord.SelectOption(label="Rocket League",              value="1490768309522530534"),  
                discord.SelectOption(label="Genshin Impact",             value="1490768318687219945"),  
                discord.SelectOption(label="Where the Winds Meet",       value="1490768322818609314"),  
                discord.SelectOption(label="Once Human",                 value="1490768327306510449"),  
                discord.SelectOption(label="Yu-Gi-Oh!",                  value="1490768331215470592"),  
                discord.SelectOption(label="Overwatch",                  value="1490768336416411688"),  
                discord.SelectOption(label="COD",                        value="1490768340380160061"),  
                discord.SelectOption(label="Roblox",                     value="1490768345002147930"),  
                discord.SelectOption(label="League of Legends",          value="1490771688890306650"),  
                discord.SelectOption(label="Helldivers",                 value="1490779127664476310"),  
            ]
        )


class colorRoles(RoleSelect):

    def __init__(self, booster_role_id: int):
        # FIX: Booster-Rolle ID wird gespeichert für den Check im Callback
        self.booster_role_id = booster_role_id
        super().__init__(
            custom_id="select_color",
            placeholder="Farbe",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Türkis",     value="44"),                
                discord.SelectOption(label="Babyblau",   value="45"),                
                discord.SelectOption(label="Blau",       value="46"),                
                discord.SelectOption(label="Pink",       value="47"),                
                discord.SelectOption(label="Lavendel",   value="48"),                
                discord.SelectOption(label="Lila",       value="49"),                
                discord.SelectOption(label="Dunkelgrün", value="50"),                
                discord.SelectOption(label="Grün",       value="51"),                
                discord.SelectOption(label="Hellgrün",   value="52"),                
                discord.SelectOption(label="Gold",       value="53"),                
                discord.SelectOption(label="Gelb",       value="54"),                
                discord.SelectOption(label="Vanille",    value="55"),                
                discord.SelectOption(label="Orange",     value="56"),                
                discord.SelectOption(label="Rot",        value="57"),                
                discord.SelectOption(label="Bordeaux",   value="58"),                
                discord.SelectOption(label="Schwarz",    value="59"),
                ]
        )


    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id) if guild else None

        if member is None:
            await interaction.response.send_message("Member nicht gefunden.", ephemeral=True)
            return

        booster_role = guild.get_role(self.booster_role_id)
        if booster_role is None or booster_role not in member.roles:
            await interaction.response.send_message(
                "Diese Farbrollen sind nur für **Server Booster** verfügbar!",
                ephemeral=True
            )
            return

        await super().callback(interaction)


class RoleView01(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenderRoles())
        self.add_item(AgeRoles())
        self.add_item(StateRoles())
        self.add_item(DM_StatusRoles())


class RoleView02(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GamesRoles())
        self.add_item(PingRoles())


class color_booster(discord.ui.View):

    def __init__(self, booster_role_id: int):
        super().__init__(timeout=None)
        self.add_item(colorRoles(booster_role_id))